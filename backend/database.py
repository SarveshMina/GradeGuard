# database.py

import os
import uuid
from azure.cosmos import CosmosClient
from typing import List, Dict, Any

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DBNAME = os.environ.get("COSMOS_DBNAME")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER")  # e.g., "users"
COSMOS_UNI_CONTAINER = os.environ.get("COSMOS_UNI_CONTAINER")  # e.g. "universities"
COSMOS_EVENTS_CONTAINER = os.environ.get("COSMOS_EVENTS_CONTAINER", "events")


_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
_db = _client.get_database_client(COSMOS_DBNAME)

_container = _db.get_container_client(COSMOS_CONTAINER)
_uni_container = _db.get_container_client(COSMOS_UNI_CONTAINER)
_events_container = _db.get_container_client(COSMOS_EVENTS_CONTAINER)

def create_user(user_dict: dict):
    _container.create_item(user_dict)

def get_user_by_email(email: str):
    try:
        user_doc = _container.read_item(item=email, partition_key=email)
        return user_doc
    except Exception:
        return None

def get_user_modules(email: str) -> List[Dict[str, Any]]:
    """Retrieve modules for a user"""
    query = f"SELECT * FROM c WHERE c.type = 'module' AND c.user_email = '{email}'"
    modules = list(_container.query_items(query=query, enable_cross_partition_query=True))
    return modules

def increment_university_and_major_counter(university_name: str, major_name: str):
    """
    Increments counters for university and major, handling the case when the university
    already exists in a different document.
    """
    try:
        # First, query for the university by name (instead of trying to read directly)
        query = f"SELECT * FROM c WHERE c.name = '{university_name}'"
        items = list(_uni_container.query_items(query=query, enable_cross_partition_query=True))
        
        # If we found items, use the first one
        if items:
            uni_doc = items[0]
        else:
            # Create a new university document
            uni_doc = {
                "id": university_name,  # Use name as ID
                "name": university_name,
                "counter": 0,
                "majors": []
            }
        
        # Increment the counter
        uni_doc["counter"] = uni_doc.get("counter", 0) + 1
        
        # Check if the major exists
        major_found = None
        for m in uni_doc.get("majors", []):
            if m["major_name"].lower() == major_name.lower():
                major_found = m
                break
        
        # If major found, increment counter, otherwise add it
        if major_found:
            major_found["counter"] += 1
        else:
            if "majors" not in uni_doc:
                uni_doc["majors"] = []
            
            uni_doc["majors"].append({
                "major_name": major_name,
                "counter": 1
            })
        
        # Upsert (update or insert) the document
        _uni_container.upsert_item(uni_doc)
        
    except Exception as e:
        print(f"Error updating university counter: {str(e)}")
        # Don't raise the exception - we don't want user registration to fail
        # if the counter update fails

def get_all_universities_docs():
    query = "SELECT * FROM c"
    items = list(_uni_container.query_items(query=query, enable_cross_partition_query=True))
    return items

def get_university_doc(university_name: str):
    try:
        doc = _uni_container.read_item(item=university_name, partition_key=university_name)
        return doc
    except:
        return None

def update_user_calculator(email: str, calculator_config: dict):
    user_doc = get_user_by_email(email)
    if not user_doc:
        raise Exception("User not found")
    user_doc["calculator"] = calculator_config
    _container.upsert_item(user_doc)

def search_universities(query: str, limit: int = 10, offset: int = 0):
    query_lower = query.lower()
    query_str = "SELECT * FROM c WHERE CONTAINS(LOWER(c.name), @query)"
    parameters = [{"name": "@query", "value": query_lower}]
    items = list(_uni_container.query_items(query=query_str, parameters=parameters, enable_cross_partition_query=True))
    return items[offset:offset+limit]


def create_calendar_event(user_email: str, event_data: dict):
    # Generate ID if not provided
    if not event_data.get('id'):
        event_data['id'] = str(uuid.uuid4())
    
    event_data['user_email'] = user_email
    
    # Create composite key for partitioning
    event_id = event_data['id']
    event_data['pk'] = f"{user_email}:{event_id}"
    
    print(f"Creating event with ID: {event_id} and partition key: {event_data['pk']}")
    
    created_item = _events_container.create_item(body=event_data)
    return created_item  # Return the actual created item from the database

def get_user_events(user_email: str, start_date: str = None, end_date: str = None):
    query = "SELECT * FROM c WHERE c.user_email = @email"
    params = [{"name": "@email", "value": user_email}]
    
    if start_date and end_date:
        query += " AND c.date >= @start AND c.date <= @end"
        params.extend([
            {"name": "@start", "value": start_date},
            {"name": "@end", "value": end_date}
        ])
    
    events = list(_events_container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))
    return events

def update_calendar_event(user_email: str, event_id: str, update_data: dict):
    pk = f"{user_email}:{event_id}"
    try:
        # Try to get the existing event with the constructed partition key
        print(f"Attempting to read event with ID: {event_id} and partition key: {pk}")
        event = _events_container.read_item(item=event_id, partition_key=pk)
        
        # Update fields
        for key, value in update_data.items():
            if key not in ['id', 'user_email', 'pk']:
                event[key] = value
        
        # Save updates
        return _events_container.replace_item(item=event_id, body=event)
    except Exception as e:
        print(f"Error updating with direct approach: {str(e)}")
        
        try:
            # If direct update fails, try to find the event by query first
            query = f"SELECT * FROM c WHERE c.id = '{event_id}' AND c.user_email = '{user_email}'"
            items = list(_events_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            if items:
                event = items[0]
                print(f"Found item by query: {event}")
                
                # Update fields
                for key, value in update_data.items():
                    if key not in ['id', 'user_email', 'pk']:
                        event[key] = value
                
                # Use the actual partition key from the found item
                actual_pk = event.get("pk", pk)
                print(f"Using actual partition key: {actual_pk}")
                
                # Save updates
                return _events_container.replace_item(item=event_id, body=event)
            else:
                print(f"Event with ID {event_id} not found in database")
                raise Exception("Event not found")
                
        except Exception as query_error:
            print(f"Error in query approach: {str(query_error)}")
            raise query_error

def delete_calendar_event(user_email: str, event_id: str):
    """Delete a calendar event with improved error handling and troubleshooting."""
    try:
        # First try to find the event to verify it exists and get its actual structure
        query = f"SELECT * FROM c WHERE c.id = '{event_id}' AND c.user_email = '{user_email}'"
        items = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if not items:
            print(f"Event with ID {event_id} not found for user {user_email}")
            return False
            
        # Get the event and inspect its structure
        event = items[0]
        print(f"Found event to delete: {event}")
        
        # Try different partition key strategies
        
        # 1. Try using event ID as partition key (common pattern)
        try:
            print(f"Attempting to delete with event ID as partition key")
            _container.delete_item(item=event_id, partition_key=event_id)
            return True
        except Exception as e:
            print(f"Failed with event ID as partition key: {str(e)}")
        
        # 2. Try user_email as partition key
        try:
            print(f"Attempting to delete with user_email as partition key")
            _container.delete_item(item=event_id, partition_key=user_email)
            return True
        except Exception as e:
            print(f"Failed with user_email as partition key: {str(e)}")
        
        # 3. Try composite key if it exists in the event
        if "pk" in event:
            try:
                print(f"Attempting to delete with pk={event['pk']} from event")
                _container.delete_item(item=event_id, partition_key=event["pk"])
                return True
            except Exception as e:
                print(f"Failed with pk from event: {str(e)}")
        
        # 4. Try the composite key format
        composite_key = f"{user_email}:{event_id}"
        try:
            print(f"Attempting to delete with composite key: {composite_key}")
            _container.delete_item(item=event_id, partition_key=composite_key)
            return True
        except Exception as e:
            print(f"Failed with composite key: {str(e)}")
        
        # If we got here, all delete attempts failed
        print("All deletion methods failed. Check Cosmos DB configuration.")
        return False
        
    except Exception as e:
        print(f"Error in delete_calendar_event: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

# Add this helper function to get modules with statistics
def get_modules_with_stats(university: str, degree: str):
    """Get modules with statistics for a specific university and degree"""
    try:
        # Query for modules of this university and degree
        query = f"""
        SELECT c.name, c.code, c.credits, c.year, c.semester,
               AVG(c.score) as average_score,
               COUNT(c.id) as student_count
        FROM c
        WHERE c.type = 'module'
          AND c.university = '{university}'
          AND c.degree = '{degree}'
        GROUP BY c.name, c.code, c.credits, c.year, c.semester
        """
        
        modules = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        return modules
    except Exception as e:
        print(f"Error getting modules with stats: {str(e)}")
        return []