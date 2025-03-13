# ical_service.py
import os
import uuid
import logging
import datetime
import pytz
import requests
import re
import icalendar
from typing import List, Dict, Any, Optional, Tuple
from dateutil.rrule import rrulestr
from dateutil.parser import parse
from io import StringIO

from models import ImportedCalendar, StudySession
from database import _container, get_user_by_email

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Storage for storing export files
STORAGE_CONNECTION_STRING = os.environ.get("STORAGE_CONNECTION_STRING")
STORAGE_CONTAINER_NAME = os.environ.get("CALENDAR_STORAGE_CONTAINER_NAME", "user-calendars")

def get_user_imported_calendars(user_email: str) -> List[ImportedCalendar]:
    """
    Get a list of the user's imported calendars.
    
    Args:
        user_email: User's email address
    
    Returns:
        List of imported calendars
    """
    try:
        query = f"SELECT * FROM c WHERE c.type = 'imported_calendar' AND c.user_email = '{user_email}'"
        
        calendars = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        return [ImportedCalendar(**calendar) for calendar in calendars]
    except Exception as e:
        logger.error(f"Error retrieving imported calendars: {str(e)}")
        return []

def import_ical_from_url(user_email: str, calendar_name: str, url: str) -> Dict[str, Any]:
    """
    Import an iCal calendar from a URL.
    
    Args:
        user_email: User's email
        calendar_name: Name for the imported calendar
        url: URL to the iCal file
        
    Returns:
        Dictionary with import results
    """
    try:
        # Check for existing calendar with this name
        query = f"SELECT * FROM c WHERE c.type = 'imported_calendar' AND c.user_email = '{user_email}' AND c.name = '{calendar_name}'"
        
        existing_calendars = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        # If calendar exists, update URL
        if existing_calendars:
            calendar = existing_calendars[0]
            calendar["url"] = url
            calendar["last_sync"] = datetime.datetime.utcnow().isoformat()
            
            _container.upsert_item(body=calendar)
            calendar_id = calendar["id"]
        else:
            # Create new imported calendar
            calendar = {
                "id": str(uuid.uuid4()),
                "type": "imported_calendar",
                "user_email": user_email,
                "name": calendar_name,
                "url": url,
                "last_sync": datetime.datetime.utcnow().isoformat(),
                "sync_frequency": "daily",
                "enabled": True
            }
            
            _container.create_item(body=calendar)
            calendar_id = calendar["id"]
        
        # Import events from the calendar
        events, modules = import_ical_events(user_email, url)
        
        # Return import results
        return {
            "calendar_id": calendar_id,
            "events_imported": len(events),
            "modules_detected": len(modules),
            "modules": modules
        }
        
    except Exception as e:
        logger.error(f"Error importing iCal calendar: {str(e)}")
        return {
            "error": str(e),
            "events_imported": 0,
            "modules_detected": 0
        }

def import_ical_events(user_email: str, url: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Import events from an iCal file and detect modules.
    
    Args:
        user_email: User's email
        url: URL to the iCal file
        
    Returns:
        Tuple of (list of imported events, list of detected modules)
    """
    try:
        # Fetch the iCal file
        response = requests.get(url)
        response.raise_for_status()
        
        ical_text = response.text
        
        return _process_ical_content(user_email, ical_text)
        
    except Exception as e:
        logger.error(f"Error importing iCal events: {str(e)}")
        return [], []

def import_ical_from_file(user_email: str, calendar_name: str, file_content: str) -> Dict[str, Any]:
    """
    Import an iCal calendar from file content.
    
    Args:
        user_email: User's email
        calendar_name: Name for the imported calendar
        file_content: String content of the iCal file
        
    Returns:
        Dictionary with import results
    """
    try:
        # Create new imported calendar
        calendar = {
            "id": str(uuid.uuid4()),
            "type": "imported_calendar",
            "user_email": user_email,
            "name": calendar_name,
            "url": None,  # No URL since it's from a file
            "last_sync": datetime.datetime.utcnow().isoformat(),
            "sync_frequency": None,  # No sync frequency for file imports
            "enabled": True
        }
        
        _container.create_item(body=calendar)
        calendar_id = calendar["id"]
        
        # Import events from the calendar
        events, modules = _process_ical_content(user_email, file_content)
        
        # Return import results
        return {
            "calendar_id": calendar_id,
            "events_imported": len(events),
            "modules_detected": len(modules),
            "modules": modules
        }
        
    except Exception as e:
        logger.error(f"Error importing iCal from file: {str(e)}")
        return {
            "error": str(e),
            "events_imported": 0,
            "modules_detected": 0
        }

def _process_ical_content(user_email: str, ical_text: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Process iCal content to extract events and detect modules.
    
    Args:
        user_email: User's email
        ical_text: iCal file content as string
        
    Returns:
        Tuple of (list of imported events, list of detected modules)
    """
    try:
        # Parse the iCal file
        cal = icalendar.Calendar.from_ical(ical_text)
        
        events = []
        module_patterns = {}  # Store potential module patterns
        
        # Get existing calendar events to avoid duplicates
        existing_events_query = f"SELECT c.id, c.title, c.date FROM c WHERE c.user_email = '{user_email}'"
        existing_events = list(_container.query_items(
            query=existing_events_query,
            enable_cross_partition_query=True
        ))
        
        # Create a set of date+title combinations for quick duplicate checking
        existing_event_keys = {f"{e['date']}|{e['title']}" for e in existing_events}
        
        # Process each event
        for component in cal.walk():
            if component.name == "VEVENT":
                # Extract event details
                summary = str(component.get('summary', ''))
                
                # Skip events with empty summary
                if not summary:
                    continue
                
                # Get the event start time
                dtstart = component.get('dtstart').dt
                
                # Handle all-day events
                all_day = False
                if isinstance(dtstart, datetime.date) and not isinstance(dtstart, datetime.datetime):
                    all_day = True
                    start_time = None
                    end_time = None
                    event_date = dtstart.isoformat()
                else:
                    # Convert to UTC and then to local time if timezone info is present
                    if dtstart.tzinfo:
                        dtstart = dtstart.astimezone(pytz.UTC)
                    
                    # Extract date and time components
                    event_date = dtstart.date().isoformat()
                    start_time = dtstart.strftime("%H:%M")
                    
                    # Get end time if available
                    if component.get('dtend'):
                        dtend = component.get('dtend').dt
                        if dtend.tzinfo:
                            dtend = dtend.astimezone(pytz.UTC)
                        end_time = dtend.strftime("%H:%M")
                    else:
                        # Default to 1 hour duration
                        end_time = (dtstart + datetime.timedelta(hours=1)).strftime("%H:%M")
                
                # Add location if available
                location = str(component.get('location', ''))
                
                # Create description
                description = str(component.get('description', ''))
                
                # Create event ID
                event_id = str(uuid.uuid4())
                
                # Create event dict
                event = {
                    "id": event_id,
                    "type": "calendar_event",
                    "user_email": user_email,
                    "title": summary,
                    "description": description,
                    "location": location,
                    "date": event_date,
                    "all_day": all_day
                }
                
                if not all_day:
                    event["start_time"] = start_time
                    event["end_time"] = end_time
                
                # Check for duplicates
                event_key = f"{event_date}|{summary}"
                if event_key in existing_event_keys:
                    continue
                
                # Add this event to our existing keys to avoid internal duplicates
                existing_event_keys.add(event_key)
                
                # Check if this looks like a module class
                module_name = _detect_module_from_event(summary, description, location)
                if module_name:
                    if module_name not in module_patterns:
                        module_patterns[module_name] = {
                            "name": module_name,
                            "event_count": 0,
                            "locations": set(),
                            "likely_module": False
                        }
                    
                    # Update pattern data
                    module_patterns[module_name]["event_count"] += 1
                    if location:
                        module_patterns[module_name]["locations"].add(location)
                    
                    # If we see a pattern multiple times, mark as likely module
                    if module_patterns[module_name]["event_count"] >= 2:
                        module_patterns[module_name]["likely_module"] = True
                    
                    # Add module metadata to event
                    event["detected_module"] = module_name
                
                # Apply recurrence if present
                if 'RRULE' in component:
                    recurrence_events = _expand_recurrence(component, event)
                    events.extend(recurrence_events)
                else:
                    # Save the event
                    try:
                        _container.create_item(body=event)
                        events.append(event)
                    except Exception as e:
                        logger.error(f"Error saving event {event_id}: {str(e)}")
        
        # Process module patterns
        detected_modules = []
        for module_name, data in module_patterns.items():
            if data["likely_module"]:
                module_info = {
                    "name": module_name,
                    "occurrence_count": data["event_count"],
                    "locations": list(data["locations"]),
                    "confidence": "high" if data["event_count"] > 3 else "medium"
                }
                detected_modules.append(module_info)
        
        return events, detected_modules
        
    except Exception as e:
        logger.error(f"Error processing iCal content: {str(e)}")
        return [], []

def _detect_module_from_event(summary: str, description: str, location: str) -> Optional[str]:
    """
    Attempt to detect a module name from an event.
    
    Args:
        summary: Event summary/title
        description: Event description
        location: Event location
        
    Returns:
        Detected module name or None
    """
    # Common patterns for module codes
    module_code_pattern = re.compile(r'([A-Z]{2,4}[0-9]{3,5})')
    
    # Check summary for module code
    code_match = module_code_pattern.search(summary)
    if code_match:
        # Extract text around the module code
        module_name = summary
        
        # Clean up the module name
        module_name = re.sub(r'\s*[\-:]\s*', ' - ', module_name)
        module_name = re.sub(r'\s+', ' ', module_name).strip()
        
        return module_name
    
    # Look for keywords that suggest this is a lecture, seminar, etc.
    academic_keywords = ['lecture', 'seminar', 'tutorial', 'lab', 'laboratory', 'workshop', 'class']
    
    for keyword in academic_keywords:
        if keyword.lower() in summary.lower():
            return summary
    
    # Not detected as a module
    return None

def _expand_recurrence(component, base_event) -> List[Dict[str, Any]]:
    """
    Expand a recurring event to individual instances.
    
    Args:
        component: iCalendar component with recurrence rule
        base_event: Base event dictionary
        
    Returns:
        List of expanded event instances
    """
    try:
        events = []
        
        # Get the recurrence rule
        rrule_str = component.get('RRULE').to_ical().decode('utf-8')
        
        # Get the start date
        dtstart = component.get('dtstart').dt
        
        # Convert date to datetime if needed
        if isinstance(dtstart, datetime.date) and not isinstance(dtstart, datetime.datetime):
            dtstart = datetime.datetime.combine(dtstart, datetime.time(0, 0))
        
        # Set up rule with the start date
        rule = rrulestr(rrule_str, dtstart=dtstart)
        
        # Get exdates (exception dates)
        exdates = []
        if 'EXDATE' in component:
            for exdate in component.get('EXDATE', []):
                if isinstance(exdate, list):
                    exdates.extend([date.dt for date in exdate])
                else:
                    exdates.append(exdate.dt)
        
        # Get recurrence instances (limit to reasonable future)
        end_date = datetime.datetime.now() + datetime.timedelta(days=365)
        instances = rule.between(dtstart, end_date)
        
        # Create events for each instance
        for instance in instances:
            # Skip exception dates
            if instance in exdates:
                continue
            
            # Create a new event for this instance
            event = base_event.copy()
            event["id"] = str(uuid.uuid4())
            
            # Update date for this instance
            if base_event["all_day"]:
                event["date"] = instance.date().isoformat()
            else:
                event["date"] = instance.date().isoformat()
                
                # Keep the same time components
                start_time_parts = base_event["start_time"].split(":")
                end_time_parts = base_event["end_time"].split(":")
                
                # Combine date and time
                start_dt = datetime.datetime.combine(
                    instance.date(),
                    datetime.time(int(start_time_parts[0]), int(start_time_parts[1]))
                )
                
                end_dt = datetime.datetime.combine(
                    instance.date(),
                    datetime.time(int(end_time_parts[0]), int(end_time_parts[1]))
                )
                
                # If end time is earlier than start time, assume it's on the next day
                if end_dt < start_dt:
                    end_dt += datetime.timedelta(days=1)
                
                # Update times
                event["start_time"] = start_dt.strftime("%H:%M")
                event["end_time"] = end_dt.strftime("%H:%M")
            
            # Add recurrence info
            event["recurrence_id"] = base_event["id"]
            
            # Save the event
            try:
                _container.create_item(body=event)
                events.append(event)
            except Exception as e:
                logger.error(f"Error saving recurring event {event['id']}: {str(e)}")
        
        return events
        
    except Exception as e:
        logger.error(f"Error expanding recurrence: {str(e)}")
        return []

def generate_ical_export(user_email: str, include_study_sessions: bool = True) -> str:
    """
    Generate an iCal export of the user's calendar.
    
    Args:
        user_email: User's email
        include_study_sessions: Whether to include AI-generated study sessions
        
    Returns:
        iCal file content as string
    """
    try:
        # Create calendar
        cal = icalendar.Calendar()
        cal.add('prodid', '-//GradeGuard//EN')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        
        # Get user events
        query = f"SELECT * FROM c WHERE c.user_email = '{user_email}'"
        
        if not include_study_sessions:
            query += " AND NOT IS_DEFINED(c.is_ai_generated)"
        
        events = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        # Add events to calendar
        for event in events:
            # Skip if not a calendar event or study session
            if "type" not in event or (event["type"] != "calendar_event" and event["type"] != "study_session"):
                continue
            
            # Create iCal event
            ical_event = icalendar.Event()
            
            # Add UID
            ical_event.add('uid', event["id"])
            
            # Add summary
            ical_event.add('summary', event["title"])
            
            # Add description if available
            if "description" in event and event["description"]:
                ical_event.add('description', event["description"])
            
            # Add location if available
            if "location" in event and event["location"]:
                ical_event.add('location', event["location"])
            
            # Add start and end times
            event_date = datetime.date.fromisoformat(event["date"])
            
            if event.get("all_day", False):
                # All-day event
                ical_event.add('dtstart', event_date)
                ical_event.add('dtend', event_date + datetime.timedelta(days=1))
            else:
                # Timed event
                start_time = datetime.datetime.strptime(event["start_time"], "%H:%M").time()
                end_time = datetime.datetime.strptime(event["end_time"], "%H:%M").time()
                
                start_dt = datetime.datetime.combine(event_date, start_time)
                end_dt = datetime.datetime.combine(event_date, end_time)
                
                # If end time is earlier than start time, assume it's on the next day
                if end_dt < start_dt:
                    end_dt += datetime.timedelta(days=1)
                
                ical_event.add('dtstart', start_dt)
                ical_event.add('dtend', end_dt)
            
            # Add creation timestamp
            ical_event.add('dtstamp', datetime.datetime.utcnow())
            
            # Add status
            if "status" in event:
                status_map = {
                    "scheduled": "CONFIRMED",
                    "completed": "COMPLETED",
                    "cancelled": "CANCELLED",
                    "missed": "CANCELLED"
                }
                
                ical_status = status_map.get(event["status"], "CONFIRMED")
                ical_event.add('status', ical_status)
            
            # Add additional metadata
            if "is_ai_generated" in event and event["is_ai_generated"]:
                ical_event.add('x-gradeguard-generated', "true")
            
            if "module_name" in event:
                ical_event.add('x-gradeguard-module', event["module_name"])
            
            # Add to calendar
            cal.add_component(ical_event)
        
        # Generate iCal content
        ical_content = cal.to_ical().decode('utf-8')
        
        return ical_content
        
    except Exception as e:
        logger.error(f"Error generating iCal export: {str(e)}")
        return ""

def create_ical_export_url(user_email: str) -> str:
    """
    Create a shareable URL for the user's iCal export.
    
    Args:
        user_email: User's email
        
    Returns:
        URL for the iCal export
    """
    try:
        from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
        
        # Check if storage connection is available
        if not STORAGE_CONNECTION_STRING:
            raise ValueError("Storage connection string not configured")
        
        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        
        # Create container if it doesn't exist
        try:
            container_client = blob_service_client.get_container_client(STORAGE_CONTAINER_NAME)
            container_client.get_container_properties()
        except Exception:
            container_client = blob_service_client.create_container(STORAGE_CONTAINER_NAME, public_access="blob")
        
        # Create a unique blob name
        token = str(uuid.uuid4())
        user_id_safe = user_email.replace("@", "-at-").replace(".", "-")
        blob_name = f"calendar-{user_id_safe}-{token}.ics"
        
        # Generate iCal content
        ical_content = generate_ical_export(user_email)
        
        # Upload to blob storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(ical_content, overwrite=True)
        
        # Generate SAS token for read access that doesn't expire for a year
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=STORAGE_CONTAINER_NAME,
            blob_name=blob_name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.datetime.utcnow() + datetime.timedelta(days=365)
        )
        
        # Generate full URL
        url = f"{blob_client.url}?{sas_token}"
        
        # Save URL in user settings
        query = f"SELECT * FROM c WHERE c.id = '{user_email}'"
        users = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if users:
            user = users[0]
            
            # Initialize scheduler settings if not exists
            if "schedulerSettings" not in user:
                user["schedulerSettings"] = {
                    "ical_export_enabled": True,
                    "ical_export_url": url
                }
            else:
                user["schedulerSettings"]["ical_export_enabled"] = True
                user["schedulerSettings"]["ical_export_url"] = url
            
            _container.upsert_item(body=user)
        
        return url
        
    except Exception as e:
        logger.error(f"Error creating iCal export URL: {str(e)}")
        return ""

def update_calendar_exports() -> Dict[str, Any]:
    """
    Background process to update all users' calendar exports.
    
    Returns:
        Status report
    """
    try:
        # Find users with export enabled
        query = "SELECT c.id, c.email FROM c WHERE IS_DEFINED(c.schedulerSettings) AND c.schedulerSettings.ical_export_enabled = true"
        
        users = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        updated_count = 0
        failed_count = 0
        
        for user in users:
            user_email = user["id"]
            
            try:
                # Regenerate export URL
                url = create_ical_export_url(user_email)
                
                if url:
                    updated_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"Error updating export for user {user_email}: {str(e)}")
                failed_count += 1
        
        return {
            "users_processed": len(users),
            "exports_updated": updated_count,
            "exports_failed": failed_count
        }
        
    except Exception as e:
        logger.error(f"Error updating calendar exports: {str(e)}")
        return {
            "error": str(e),
            "users_processed": 0,
            "exports_updated": 0,
            "exports_failed": 0
        }

def sync_imported_calendars() -> Dict[str, Any]:
    """
    Background process to sync all imported calendars.
    
    Returns:
        Status report
    """
    try:
        # Find all imported calendars with URLs
        query = "SELECT * FROM c WHERE c.type = 'imported_calendar' AND IS_DEFINED(c.url) AND c.enabled = true"
        
        calendars = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        synced_count = 0
        failed_count = 0
        total_events = 0
        
        for calendar in calendars:
            try:
                # Skip if last sync was recent (based on frequency)
                if "last_sync" in calendar:
                    last_sync = datetime.datetime.fromisoformat(calendar["last_sync"].replace('Z', '+00:00'))
                    now = datetime.datetime.utcnow()
                    
                    if calendar["sync_frequency"] == "daily":
                        if (now - last_sync).days < 1:
                            continue
                    elif calendar["sync_frequency"] == "weekly":
                        if (now - last_sync).days < 7:
                            continue
                
                # Sync the calendar
                events, _ = import_ical_events(calendar["user_email"], calendar["url"])
                
                # Update last sync time
                calendar["last_sync"] = datetime.datetime.utcnow().isoformat()
                _container.upsert_item(body=calendar)
                
                synced_count += 1
                total_events += len(events)
                
            except Exception as e:
                logger.error(f"Error syncing calendar {calendar['id']}: {str(e)}")
                failed_count += 1
        
        return {
            "calendars_processed": len(calendars),
            "calendars_synced": synced_count,
            "calendars_failed": failed_count,
            "events_imported": total_events
        }
        
    except Exception as e:
        logger.error(f"Error syncing imported calendars: {str(e)}")
        return {
            "error": str(e),
            "calendars_processed": 0,
            "calendars_synced": 0,
            "calendars_failed": 0,
            "events_imported": 0
        }

def import_events_to_user_module_map(user_email: str) -> Dict[str, List[str]]:
    """
    Create a mapping of module patterns to module IDs based on event titles.
    
    Args:
        user_email: User's email
        
    Returns:
        Dictionary mapping event module names to actual module IDs
    """
    try:
        # Get events that have a detected module
        event_query = f"""
        SELECT c.detected_module
        FROM c
        WHERE c.user_email = '{user_email}' 
        AND IS_DEFINED(c.detected_module)
        GROUP BY c.detected_module
        """
        
        events = list(_container.query_items(
            query=event_query,
            enable_cross_partition_query=True
        ))
        
        # Get user modules
        module_query = f"SELECT c.id, c.name, c.code FROM c WHERE c.type = 'module' AND c.user_email = '{user_email}'"
        
        modules = list(_container.query_items(
            query=module_query,
            enable_cross_partition_query=True
        ))
        
        # Create mapping
        module_map = {}
        
        for event in events:
            module_name = event["detected_module"]
            
            # Find matching module
            matches = []
            for module in modules:
                # Check for exact name match
                if module["name"].lower() == module_name.lower():
                    matches.append(module["id"])
                    break
                
                # Check for code match if available
                if "code" in module and module["code"]:
                    if module["code"] in module_name:
                        matches.append(module["id"])
                        break
                
                # Check for partial name match
                if module["name"].lower() in module_name.lower() or module_name.lower() in module["name"].lower():
                    matches.append(module["id"])
            
            # Add mapping
            if matches:
                module_map[module_name] = matches
            else:
                module_map[module_name] = []
        
        return module_map
        
    except Exception as e:
        logger.error(f"Error creating module mapping: {str(e)}")
        return {}