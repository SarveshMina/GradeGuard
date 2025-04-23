# database.py

import os
import uuid
from azure.cosmos import CosmosClient
from datetime import datetime
import json
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
    """Delete a calendar event with improved query"""
    try:
        # Use parameterized query for security
        query = "SELECT * FROM c WHERE c.id = @event_id AND c.user_email = @user_email"
        params = [
            {"name": "@event_id", "value": event_id},
            {"name": "@user_email", "value": user_email}
        ]

        items = list(_events_container.query_items(
            query=query,
            parameters=params,
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
            _events_container.delete_item(item=event_id, partition_key=event_id)
            return True
        except Exception as e:
            print(f"Failed with event ID as partition key: {str(e)}")

        # 2. Try user_email as partition key
        try:
            print(f"Attempting to delete with user_email as partition key")
            _events_container.delete_item(item=event_id, partition_key=user_email)
            return True
        except Exception as e:
            print(f"Failed with user_email as partition key: {str(e)}")

        # 3. Try composite key if it exists in the event
        if "pk" in event:
            try:
                print(f"Attempting to delete with pk={event['pk']} from event")
                _events_container.delete_item(item=event_id, partition_key=event["pk"])
                return True
            except Exception as e:
                print(f"Failed with pk from event: {str(e)}")

        # 4. Try the composite key format
        composite_key = f"{user_email}:{event_id}"
        try:
            print(f"Attempting to delete with composite key: {composite_key}")
            _events_container.delete_item(item=event_id, partition_key=composite_key)
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
    
def get_module_reviews(module_id: str):
    """Get all reviews for a specific module"""
    query = "SELECT * FROM c WHERE c.type = 'module_review' AND c.module_id = @module_id"
    parameters = [{"name": "@module_id", "value": module_id}]
    
    reviews = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return reviews

def create_module_review(review_data: dict):
    """Create a new module review"""
    # Add metadata
    review_data["type"] = "module_review"
    if "id" not in review_data:
        review_data["id"] = f"review_{str(uuid.uuid4())}"
    review_data["created_at"] = datetime.utcnow().isoformat()
    
    # Create in database
    result = _container.create_item(body=review_data)
    
    # Update module statistics
    update_module_statistics(review_data["module_id"], review_data["university"], review_data["degree"])
    
    return result

def delete_module_review(review_id: str, user_email: str):
    """Delete a module review (only by the creator)"""
    query = "SELECT * FROM c WHERE c.id = @id AND c.user_email = @email AND c.type = 'module_review'"
    parameters = [
        {"name": "@id", "value": review_id},
        {"name": "@email", "value": user_email}
    ]
    
    reviews = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    
    if not reviews:
        return False
    
    # Get the module_id for updating statistics later
    module_id = reviews[0].get("module_id")
    university = reviews[0].get("university")
    degree = reviews[0].get("degree")
    
    # Delete the review
    _container.delete_item(item=review_id, partition_key=review_id)
    
    # Update module statistics
    update_module_statistics(module_id, university, degree)
    
    return True

def get_module_statistics(module_id: str, university: str, degree: str):
    """Calculate statistics for a module"""
    # Get all reviews for the module
    reviews = get_module_reviews(module_id)
    
    if not reviews:
        return {
            "difficulty_avg": 0,
            "teaching_quality_avg": 0,
            "recommended_avg": 0,
            "total_reviews": 0,
            "grade_distribution": {}
        }
    
    # Calculate average ratings
    total_difficulty = sum(r.get("difficulty_rating", 0) for r in reviews)
    total_teaching = sum(r.get("teaching_quality_rating", 0) for r in reviews)
    total_recommended = sum(r.get("recommended_rating", 0) for r in reviews)
    
    difficulty_avg = round(total_difficulty / len(reviews), 1) if reviews else 0
    teaching_avg = round(total_teaching / len(reviews), 1) if reviews else 0
    recommended_avg = round(total_recommended / len(reviews), 1) if reviews else 0
    
    # Calculate grade distribution
    grade_distribution = {}
    for review in reviews:
        if "grade_received" in review and review["grade_received"]:
            grade_range = get_grade_range(review["grade_received"])
            if grade_range not in grade_distribution:
                grade_distribution[grade_range] = 0
            grade_distribution[grade_range] += 1
    
    return {
        "difficulty_avg": difficulty_avg,
        "teaching_quality_avg": teaching_avg,
        "recommended_avg": recommended_avg,
        "total_reviews": len(reviews),
        "grade_distribution": grade_distribution
    }

def get_grade_range(grade: int) -> str:
    """Convert grade to a range string for distribution"""
    if grade >= 90:
        return "90% +"
    elif grade >= 80:
        return "80% +"
    elif grade >= 70:
        return "70% +"
    elif grade >= 60:
        return "60% +"
    elif grade >= 50:
        return "50% +"
    elif grade >= 40:
        return "40% +"
    elif grade >= 30:
        return "30% +"
    elif grade >= 20:
        return "20% +"
    elif grade >= 10:
        return "10% +"
    else:
        return "0% +"

def update_module_statistics(module_id: str, university: str, degree: str):
    """Update module statistics in the university document"""
    try:
        # Get statistics for this module
        stats = get_module_statistics(module_id, university, degree)
        
        # Now find the module in the university document
        # First, get the university document
        query = "SELECT * FROM c WHERE c.name = @university"
        parameters = [{"name": "@university", "value": university}]
        
        universities = list(_uni_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if not universities:
            return False
            
        university_doc = universities[0]
        
        # Look for the degree and modules structure
        if "degrees" not in university_doc:
            university_doc["degrees"] = {}
            
        if degree not in university_doc["degrees"]:
            university_doc["degrees"][degree] = {"modules": {}}
            
        if "modules" not in university_doc["degrees"][degree]:
            university_doc["degrees"][degree]["modules"] = {}
            
        # Update module statistics
        university_doc["degrees"][degree]["modules"][module_id] = {
            "statistics": stats,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Save changes
        _uni_container.upsert_item(university_doc)
        
        return True
    except Exception as e:
        print(f"Error updating module statistics: {str(e)}")
        return False

def get_university_modules_with_stats(university: str, degree: str = None):
    """Get all modules for a university with their statistics"""
    # Query for the university
    query = "SELECT * FROM c WHERE c.name = @university"
    parameters = [{"name": "@university", "value": university}]
    
    universities = list(_uni_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    
    if not universities:
        return []
        
    university_doc = universities[0]
    
    # Get the modules from the university document
    modules_with_stats = []
    
    if "degrees" in university_doc:
        if degree:
            # Only get modules for the specified degree
            if degree in university_doc["degrees"]:
                degree_data = university_doc["degrees"][degree]
                if "modules" in degree_data:
                    for module_id, module_data in degree_data["modules"].items():
                        # Get the base module data
                        module_info = get_module_by_id_public(module_id)
                        if module_info:
                            # Make a copy to avoid modifying the original
                            module_dict = dict(module_info)
                            # Add statistics
                            module_dict["statistics"] = module_data.get("statistics", {})
                            modules_with_stats.append(module_dict)
        else:
            # Get modules for all degrees
            for degree_name, degree_data in university_doc["degrees"].items():
                if "modules" in degree_data:
                    for module_id, module_data in degree_data["modules"].items():
                        # Get the base module data
                        module_info = get_module_by_id_public(module_id)
                        if module_info:
                            # Make a copy to avoid modifying the original
                            module_dict = dict(module_info)
                            # Add degree info and statistics
                            module_dict["degree"] = degree_name
                            module_dict["statistics"] = module_data.get("statistics", {})
                            modules_with_stats.append(module_dict)
    
    return modules_with_stats

def get_module_by_id_public(module_id: str):
    """Get a module by ID for public consumption (without user-specific data)"""
    query = "SELECT c.id, c.name, c.code, c.credits, c.year, c.semester, c.university, c.degree, c.description FROM c WHERE c.id = @id AND c.type = 'module'"
    parameters = [{"name": "@id", "value": module_id}]
    
    modules = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    
    # Return as a dictionary, not a module object
    return dict(modules[0]) if modules else None

def get_degree_modules_with_stats(university: str, degree: str):
    """Get all modules for a specific degree with statistics"""
    return get_university_modules_with_stats(university, degree)