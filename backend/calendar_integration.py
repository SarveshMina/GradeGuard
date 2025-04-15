# calendar_integration.py
import os
import requests
import uuid
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import icalendar
from icalendar import Calendar, Event
from database import _container
from calendar_routes import create_event
from azure.functions import HttpRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CALENDAR_STORAGE_CONTAINER_NAME = os.environ.get("CALENDAR_STORAGE_CONTAINER_NAME", "user-calendars")

def parse_ical_url(ical_url: str, user_email: str) -> List[Dict[str, Any]]:
    """
    Fetch and parse an iCal feed from a URL
    Returns a list of calendar events ready to be added to the user's calendar
    """
    try:
        # Fetch the iCal file
        response = requests.get(ical_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the iCal data
        cal = Calendar.from_ical(response.content)
        
        # Extract events
        events = []
        
        for component in cal.walk():
            if component.name == "VEVENT":
                # Extract the basic event information
                summary = str(component.get('summary', 'Unnamed Event'))
                description = str(component.get('description', ''))
                
                # Handle start time
                start = component.get('dtstart').dt
                if isinstance(start, datetime):
                    start_time = start.isoformat()
                    all_day = False
                else:
                    # This is a date without time, so it's an all-day event
                    start_time = datetime.combine(start, datetime.min.time()).isoformat()
                    all_day = True
                
                # Handle end time
                end = component.get('dtend')
                if end:
                    end = end.dt
                    if isinstance(end, datetime):
                        end_time = end.isoformat()
                    else:
                        # This is a date without time
                        end_time = datetime.combine(end, datetime.min.time()).isoformat()
                else:
                    # If no end time, set to start time + 1 hour for non-all-day events
                    if all_day:
                        end_time = start_time
                    else:
                        end_time = (datetime.fromisoformat(start_time) + timedelta(hours=1)).isoformat()
                
                # Handle location
                location = str(component.get('location', ''))
                
                # Create the event dictionary
                event = {
                    "user_email": user_email,
                    "title": summary,
                    "description": description,
                    "date": start_time.split('T')[0],  # Just the date part
                    "start_time": None if all_day else start_time,
                    "end_time": None if all_day else end_time,
                    "all_day": all_day,
                    "type": detect_event_type(summary, description),
                    "location": location,
                    "source": "ical_import",
                    "ical_uid": str(component.get('uid', ''))
                }
                
                events.append(event)
        
        logger.info(f"Successfully parsed {len(events)} events from iCal feed")
        return events
        
    except requests.RequestException as e:
        logger.error(f"Error fetching iCal feed: {str(e)}")
        raise Exception(f"Failed to fetch iCal feed: {str(e)}")
    except Exception as e:
        logger.error(f"Error parsing iCal feed: {str(e)}")
        raise Exception(f"Failed to parse iCal feed: {str(e)}")

def detect_event_type(summary: str, description: str) -> str:
    """
    Detect the event type based on the summary and description
    Returns one of: class, lecture, lab, tutorial, exam, assignment, study, general
    """
    summary_lower = summary.lower()
    description_lower = description.lower()
    
    combined_text = summary_lower + " " + description_lower
    
    # Check for class-related events
    if any(word in summary_lower for word in ["lecture", "class"]):
        return "lecture"
    elif "tutorial" in summary_lower:
        return "tutorial"
    elif "lab" in summary_lower:
        return "lab"
    elif any(word in combined_text for word in ["exam", "test", "quiz", "assessment"]):
        return "exam"
    elif any(word in combined_text for word in ["assignment", "homework", "coursework", "deadline"]):
        return "assignment"
    elif "study" in combined_text:
        return "study"
    else:
        return "general"

def import_ical_events(ical_url: str, user_email: str) -> Dict[str, Any]:
    """
    Import events from an iCal feed into the user's calendar
    
    Returns a dictionary with:
    - total_events: Total number of events parsed
    - imported_events: Number of new events imported
    - updated_events: Number of existing events updated
    - skipped_events: Number of events skipped (duplicates without changes)
    """
    try:
        # Parse the iCal feed
        parsed_events = parse_ical_url(ical_url, user_email)
        
        # Track import statistics
        results = {
            "total_events": len(parsed_events),
            "imported_events": 0,
            "updated_events": 0,
            "skipped_events": 0,
            "imported_event_ids": []
        }
        
        # Check for existing events with the same iCal UID
        for event in parsed_events:
            ical_uid = event.get("ical_uid")
            
            # Skip events without a UID
            if not ical_uid:
                continue
                
            # Check if this event already exists
            query = """
            SELECT * FROM c 
            WHERE c.ical_uid = @ical_uid 
            AND c.user_email = @email
            """
            parameters = [
                {"name": "@ical_uid", "value": ical_uid},
                {"name": "@email", "value": user_email}
            ]
            
            existing_events = list(_container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            if existing_events:
                # Event already exists, check if it needs updating
                existing_event = existing_events[0]
                
                # Check if the event has changed
                if (event["title"] != existing_event.get("title") or
                    event["description"] != existing_event.get("description") or
                    event["start_time"] != existing_event.get("start_time") or
                    event["end_time"] != existing_event.get("end_time") or
                    event["location"] != existing_event.get("location")):
                    
                    # Update the existing event
                    event["id"] = existing_event["id"]
                    _container.replace_item(item=existing_event["id"], body=event)
                    results["updated_events"] += 1
                else:
                    # Event hasn't changed, skip it
                    results["skipped_events"] += 1
            else:
                # New event, create it
                event["id"] = str(uuid.uuid4())
                
                # Create the event using the calendar_routes function
                # We need to simulate an HttpRequest for this
                req_body = json.dumps(event).encode('utf-8')
                
                class MockHttpRequest:
                    def __init__(self, body):
                        self.body = body
                        
                    def get_json(self):
                        return json.loads(self.body)
                
                mock_req = MockHttpRequest(req_body)
                
                try:
                    response = create_event(mock_req, user_email)
                    
                    # Check for success
                    if 200 <= response.status_code < 300:
                        results["imported_events"] += 1
                        # Extract the created event ID from the response
                        event_data = json.loads(response.get_body().decode('utf-8'))
                        results["imported_event_ids"].append(event_data.get("id"))
                    else:
                        logger.warning(f"Failed to create event: {response.get_body().decode('utf-8')}")
                except Exception as e:
                    logger.error(f"Error creating event: {str(e)}")
        
        logger.info(f"iCal import completed: {results}")
        return results
        
    except Exception as e:
        logger.error(f"Error importing iCal events: {str(e)}")
        raise Exception(f"Failed to import iCal events: {str(e)}")

def store_ical_subscription(user_email: str, ical_url: str, name: str = "Calendar Subscription") -> Dict[str, Any]:
    """
    Store an iCal subscription for a user
    """
    try:
        # Create the subscription document
        subscription = {
            "id": f"icalsub_{uuid.uuid4()}",
            "type": "ical_subscription",
            "user_email": user_email,
            "ical_url": ical_url,
            "name": name,
            "last_sync": None,
            "created_at": datetime.utcnow().isoformat(),
            "auto_sync": True  # Enable auto-sync by default
        }
        
        # Save to database
        result = _container.create_item(body=subscription)
        return result
    except Exception as e:
        logger.error(f"Error storing iCal subscription: {str(e)}")
        raise Exception(f"Failed to store iCal subscription: {str(e)}")

def get_user_ical_subscriptions(user_email: str) -> List[Dict[str, Any]]:
    """
    Get all iCal subscriptions for a user
    """
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'ical_subscription' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        subscriptions = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return subscriptions
    except Exception as e:
        logger.error(f"Error getting iCal subscriptions: {str(e)}")
        return []

def sync_ical_subscription(subscription_id: str) -> Dict[str, Any]:
    """
    Sync events from an iCal subscription
    """
    try:
        # Get the subscription
        subscription = _container.read_item(item=subscription_id, partition_key=subscription_id)
        
        # Import events
        results = import_ical_events(subscription["ical_url"], subscription["user_email"])
        
        # Update last sync timestamp
        subscription["last_sync"] = datetime.utcnow().isoformat()
        _container.replace_item(item=subscription_id, body=subscription)
        
        # Return combined results
        return {
            "subscription": subscription,
            "sync_results": results
        }
    except Exception as e:
        logger.error(f"Error syncing iCal subscription: {str(e)}")
        raise Exception(f"Failed to sync iCal subscription: {str(e)}")

def delete_ical_subscription(subscription_id: str, user_email: str, delete_events: bool = False) -> Dict[str, Any]:
    """
    Delete an iCal subscription and optionally its events
    """
    try:
        # Get the subscription and verify ownership
        query = """
        SELECT * FROM c 
        WHERE c.id = @id 
        AND c.user_email = @email
        AND c.type = 'ical_subscription'
        """
        parameters = [
            {"name": "@id", "value": subscription_id},
            {"name": "@email", "value": user_email}
        ]
        
        results = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if not results:
            raise Exception("Subscription not found or access denied")
            
        subscription = results[0]
        
        # Delete the subscription
        _container.delete_item(item=subscription_id, partition_key=subscription_id)
        
        # If requested, delete events from this subscription
        deleted_events = 0
        if delete_events:
            query = """
            SELECT * FROM c 
            WHERE c.user_email = @email
            AND c.source = 'ical_import'
            """
            parameters = [{"name": "@email", "value": user_email}]
            
            events = list(_container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            for event in events:
                _container.delete_item(item=event["id"], partition_key=event["id"])
                deleted_events += 1
        
        return {
            "message": "Subscription deleted successfully",
            "deleted_events": deleted_events
        }
    except Exception as e:
        logger.error(f"Error deleting iCal subscription: {str(e)}")
        raise Exception(f"Failed to delete iCal subscription: {str(e)}")