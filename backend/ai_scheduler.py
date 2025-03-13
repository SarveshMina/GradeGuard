# ai_scheduler.py
import os
import uuid
import json
import datetime
import logging
from typing import List, Dict, Any, Optional
import random  # For temporary randomized schedules before implementing real AI logic

# Import OpenAI Library
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from models import StudyPreference, StudySession, SessionFeedback
from database import _container, get_user_by_email

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Standard OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "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")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4")

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

def get_user_study_preference(user_email: str) -> StudyPreference:
    """Retrieves or creates user study preferences."""
    query = f"SELECT * FROM c WHERE c.type = 'study_preference' AND c.user_email = '{user_email}'"
    
    try:
        # Query user preferences
        preferences = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if preferences:
            return StudyPreference(**preferences[0])
        
        # If no preferences found, create default
        default_preferences = StudyPreference(user_email=user_email)
        preferences_dict = default_preferences.dict()
        preferences_dict["id"] = f"study_preference_{user_email}"
        preferences_dict["type"] = "study_preference"
        
        _container.create_item(body=preferences_dict)
        return default_preferences
        
    except Exception as e:
        logger.error(f"Error retrieving study preferences: {str(e)}")
        return StudyPreference(user_email=user_email)

def get_user_sessions(user_email: str, status: Optional[str] = None, 
                     start_date: Optional[str] = None, 
                     end_date: Optional[str] = None) -> List[StudySession]:
    """Retrieves user study sessions with optional filters."""
    query = f"SELECT * FROM c WHERE c.type = 'study_session' AND c.user_email = '{user_email}'"
    
    parameters = []
    
    if status:
        query += " AND c.status = @status"
        parameters.append({"name": "@status", "value": status})
    
    if start_date:
        query += " AND c.date >= @start_date"
        parameters.append({"name": "@start_date", "value": start_date})
    
    if end_date:
        query += " AND c.date <= @end_date"
        parameters.append({"name": "@end_date", "value": end_date})
    
    try:
        sessions = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        return [StudySession(**session) for session in sessions]
    except Exception as e:
        logger.error(f"Error retrieving study sessions: {str(e)}")
        return []

def get_user_calendar_events(user_email: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Retrieves user calendar events between dates."""
    query = f"SELECT * FROM c WHERE c.user_email = '{user_email}' AND c.date >= '{start_date}' AND c.date <= '{end_date}'"
    
    try:
        events = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        # Filter out study sessions - we only want other events
        events = [event for event in events if event.get("type") != "study_session"]
        
        return events
    except Exception as e:
        logger.error(f"Error retrieving calendar events: {str(e)}")
        return []

def get_user_modules(user_email: str, status: Optional[str] = "active") -> List[Dict[str, Any]]:
    """Retrieves user modules, optionally filtering by status."""
    query = f"SELECT * FROM c WHERE c.type = 'module' AND c.user_email = '{user_email}'"
    
    if status:
        query += f" AND c.status = '{status}'"
    
    try:
        modules = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return modules
    except Exception as e:
        logger.error(f"Error retrieving modules: {str(e)}")
        return []

def _calculate_time_slots(preferences: StudyPreference) -> Dict[str, List[Dict[str, Any]]]:
    """
    Calculate available time slots based on user preferences.
    Returns a dictionary with days as keys and lists of time slots as values.
    """
    time_slots = {}
    
    # Time ranges for different parts of day
    day_parts = {
        "morning": {"start": "08:00", "end": "12:00"},
        "afternoon": {"start": "12:00", "end": "17:00"},
        "evening": {"start": "17:00", "end": "21:00"},
        "night": {"start": "21:00", "end": "23:59"}
    }
    
    # Define available slots for each preferred day
    for day in preferences.preferred_days:
        time_slots[day] = []
        
        for part in preferences.preferred_times:
            if part in day_parts:
                # Convert to datetime for easier manipulation
                start_time = datetime.datetime.strptime(day_parts[part]["start"], "%H:%M").time()
                end_time = datetime.datetime.strptime(day_parts[part]["end"], "%H:%M").time()
                
                current_time = start_time
                session_duration = datetime.timedelta(minutes=preferences.study_session_duration)
                break_duration = datetime.timedelta(minutes=preferences.breaks_between_sessions)
                
                # Create time slots
                while True:
                    dt_current = datetime.datetime.combine(datetime.date.today(), current_time)
                    dt_end = dt_current + session_duration
                    
                    # Break if we've gone past the end time for this part of day
                    if dt_end.time() > end_time:
                        break
                    
                    time_slots[day].append({
                        "start": dt_current.time().strftime("%H:%M"),
                        "end": dt_end.time().strftime("%H:%M"),
                        "part_of_day": part
                    })
                    
                    # Move to next slot (session + break)
                    dt_next = dt_end + break_duration
                    current_time = dt_next.time()
    
    return time_slots

def _filter_available_slots(time_slots: Dict[str, List[Dict[str, Any]]], 
                           busy_times: List[Dict[str, Any]],
                           excluded_times: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Filter out unavailable time slots based on existing events and excluded times.
    """
    available_slots = {day: slots.copy() for day, slots in time_slots.items()}
    
    # Convert dates to day of week
    day_map = {
        0: "monday",
        1: "tuesday",
        2: "wednesday",
        3: "thursday", 
        4: "friday",
        5: "saturday",
        6: "sunday"
    }
    
    # Filter out busy times
    for event in busy_times:
        event_date = datetime.datetime.fromisoformat(event["date"].replace('Z', '+00:00'))
        day_of_week = day_map[event_date.weekday()]
        
        if day_of_week in available_slots:
            # If all-day event, remove all slots for this day
            if event.get("all_day", False):
                available_slots[day_of_week] = []
                continue
            
            # Otherwise check for time conflicts
            if event.get("start_time") and event.get("end_time"):
                event_start = datetime.datetime.strptime(event["start_time"], "%H:%M").time()
                event_end = datetime.datetime.strptime(event["end_time"], "%H:%M").time()
                
                # Filter slots that overlap with this event
                available_slots[day_of_week] = [
                    slot for slot in available_slots[day_of_week] 
                    if not (
                        # Check if slot overlaps with event
                        (datetime.datetime.strptime(slot["start"], "%H:%M").time() < event_end and
                         datetime.datetime.strptime(slot["end"], "%H:%M").time() > event_start)
                    )
                ]
    
    # Filter out excluded times (similar logic)
    for excluded in excluded_times:
        if "day" in excluded and excluded["day"] in available_slots:
            if "all_day" in excluded and excluded["all_day"]:
                available_slots[excluded["day"]] = []
            elif "start_time" in excluded and "end_time" in excluded:
                excl_start = datetime.datetime.strptime(excluded["start_time"], "%H:%M").time()
                excl_end = datetime.datetime.strptime(excluded["end_time"], "%H:%M").time()
                
                available_slots[excluded["day"]] = [
                    slot for slot in available_slots[excluded["day"]] 
                    if not (
                        (datetime.datetime.strptime(slot["start"], "%H:%M").time() < excl_end and
                         datetime.datetime.strptime(slot["end"], "%H:%M").time() > excl_start)
                    )
                ]
    
    return available_slots

def _distribute_modules_to_slots(available_slots: Dict[str, List[Dict[str, Any]]],
                                modules: List[Dict[str, Any]],
                                preferences: StudyPreference) -> List[Dict[str, Any]]:
    """
    Distribute modules across available time slots, respecting preferences.
    """
    # Here we'll use AI to optimize, but for now use a simple algorithm
    
    # Flatten the available slots
    all_slots = []
    for day, slots in available_slots.items():
        for slot in slots:
            all_slots.append({
                "day": day,
                "start": slot["start"],
                "end": slot["end"],
                "part_of_day": slot["part_of_day"]
            })
    
    # Sort modules by importance/priority (for now, random)
    random.shuffle(modules)
    
    # Create sessions until we hit constraints
    study_sessions = []
    
    total_sessions = min(preferences.min_sessions_per_week, len(all_slots))
    
    # Weight modules by credits or importance
    module_weights = {}
    for module in modules:
        credits = module.get("credits", 15)
        # More credits = more weight
        module_weights[module["id"]] = credits / 15.0
    
    # Calculate how many sessions per module
    sessions_per_module = {}
    total_weight = sum(module_weights.values())
    
    for module_id, weight in module_weights.items():
        sessions_per_module[module_id] = max(1, int((weight / total_weight) * total_sessions))
    
    # Ensure we don't exceed total_sessions
    while sum(sessions_per_module.values()) > total_sessions:
        # Find the module with the most sessions and decrement
        max_module = max(sessions_per_module.items(), key=lambda x: x[1])[0]
        sessions_per_module[max_module] -= 1
    
    # Now assign modules to slots
    used_slots = []
    
    for module in modules:
        module_id = module["id"]
        
        # Skip if no sessions needed for this module
        if module_id not in sessions_per_module or sessions_per_module[module_id] <= 0:
            continue
        
        # Get number of sessions for this module
        num_sessions = sessions_per_module[module_id]
        
        for _ in range(num_sessions):
            if not all_slots:
                break
            
            # Find a good slot (for now, just use the first available)
            # In a real implementation, use AI to find optimal slot
            slot = all_slots.pop(0)
            used_slots.append(slot)
            
            # Create a study session
            session = {
                "id": str(uuid.uuid4()),
                "type": "study_session",
                "user_email": module["user_email"],
                "title": f"Study: {module['name']}",
                "module_id": module["id"],
                "module_name": module["name"],
                "date": _next_date_for_day(slot["day"]).isoformat(),
                "start_time": slot["start"],
                "end_time": slot["end"],
                "description": f"Study session for {module['name']}",
                "status": "scheduled",
                "is_ai_generated": True,
                "batch_id": str(uuid.uuid4())  # Same batch ID for all sessions in this generation
            }
            
            study_sessions.append(session)
    
    return study_sessions

def _next_date_for_day(day_name: str) -> datetime.date:
    """Find the next date for the given day of the week."""
    days = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    
    today = datetime.date.today()
    day_num = days.get(day_name.lower(), 0)
    days_ahead = (day_num - today.weekday()) % 7
    
    if days_ahead == 0:
        days_ahead = 7  # If today, schedule for next week
    
    return today + datetime.timedelta(days=days_ahead)

def _optimize_schedule_with_ai(user_modules: List[Dict[str, Any]], 
                               user_calendar: List[Dict[str, Any]], 
                               user_preferences: StudyPreference,
                               previous_feedback: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Use AI to optimize the study schedule based on user data and feedback.
    This is where we'll integrate with OpenAI.
    """
    if not openai.api_key:
        # If no OpenAI setup, fall back to heuristic scheduling
        logger.warning("No OpenAI API key found, falling back to heuristic scheduling")
        return None
    
    try:
        # Prepare data for OpenAI
        modules_data = json.dumps([{
            "id": m["id"],
            "name": m["name"],
            "code": m.get("code", ""),
            "credits": m.get("credits", 0),
            "score": m.get("score", 0),
            "difficulty": m.get("difficulty", "medium")
        } for m in user_modules])
        
        calendar_data = json.dumps([{
            "title": e["title"],
            "date": e["date"],
            "start_time": e.get("start_time"),
            "end_time": e.get("end_time"),
            "all_day": e.get("all_day", False)
        } for e in user_calendar])
        
        preferences_data = json.dumps(user_preferences.dict())
        
        feedback_data = "[]"
        if previous_feedback:
            feedback_data = json.dumps(previous_feedback)
        
        # Call OpenAI API
        logger.info("Calling OpenAI API to optimize schedule")
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": """You are an AI study schedule optimizer. Your task is to create an optimal study schedule
                for a student based on their modules, existing calendar commitments, preferences, and past feedback.
                Take into account:
                1. Module importance (credits, current scores, difficulty)
                2. Student's availability based on calendar
                3. Preferred study times (morning, afternoon, etc.)
                4. Previous feedback on study sessions
                5. Optimal spacing of study sessions
                
                Return your response as a JSON array of study sessions, with each session having the following format:
                {
                    "module_id": "the module id",
                    "title": "Study: Module Name",
                    "day": "monday/tuesday/etc.",
                    "date": "YYYY-MM-DD",
                    "start_time": "HH:MM",
                    "end_time": "HH:MM",
                    "description": "Brief description of the study focus"
                }
                """},
                {"role": "user", "content": f"""
                Please create an optimal study schedule based on the following data:
                
                MODULES:
                {modules_data}
                
                CALENDAR EVENTS:
                {calendar_data}
                
                USER PREFERENCES:
                {preferences_data}
                
                PREVIOUS FEEDBACK:
                {feedback_data}
                
                Return only a JSON array with the optimized study sessions.
                """}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        # Parse the response
        result = response.choices[0].message.content.strip()
        logger.info(f"Received response from OpenAI: {result[:100]}...")
        
        # Try to extract JSON if surrounded by markdown or other text
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].strip()
        
        ai_sessions = json.loads(result)
        
        # Format sessions to match our model
        batch_id = str(uuid.uuid4())  # Same batch ID for all sessions
        
        formatted_sessions = []
        for session in ai_sessions:
            # Find the module
            module = next((m for m in user_modules if m["id"] == session["module_id"]), None)
            if not module:
                continue
                
            formatted_session = {
                "id": str(uuid.uuid4()),
                "type": "study_session",
                "user_email": module["user_email"],
                "title": session.get("title", f"Study: {module['name']}"),
                "module_id": module["id"],
                "module_name": module["name"],
                "date": session["date"],
                "start_time": session["start_time"],
                "end_time": session["end_time"],
                "description": session.get("description", f"Study session for {module['name']}"),
                "status": "scheduled",
                "is_ai_generated": True,
                "batch_id": batch_id
            }
            
            formatted_sessions.append(formatted_session)
        
        logger.info(f"Successfully created {len(formatted_sessions)} study sessions with AI")
        return formatted_sessions
    
    except Exception as e:
        logger.error(f"Error optimizing schedule with AI: {str(e)}")
        return None

def generate_study_schedule(user_email: str, start_date: str = None, days_ahead: int = 14) -> List[StudySession]:
    """
    Generate a study schedule for a user based on their preferences, modules, and calendar.
    
    Args:
        user_email: The user's email
        start_date: The start date (ISO format) or today if None
        days_ahead: How many days ahead to schedule
        
    Returns:
        A list of generated study sessions
    """
    try:
        # Get user data
        preferences = get_user_study_preference(user_email)
        
        # Set date range
        if start_date is None:
            start_date = datetime.date.today().isoformat()
        
        end_date_obj = datetime.date.fromisoformat(start_date) + datetime.timedelta(days=days_ahead)
        end_date = end_date_obj.isoformat()
        
        # Get in-progress modules
        modules = get_user_modules(user_email, status="active")
        
        # Get calendar events in the date range
        calendar_events = get_user_calendar_events(user_email, start_date, end_date)
        
        # Get previous session feedback for AI optimization
        previous_sessions = get_user_sessions(user_email)
        previous_feedback = [
            {"session_id": s.id, "module_id": s.module_id, "status": s.status, "feedback": s.feedback}
            for s in previous_sessions if s.feedback is not None
        ]
        
        # Use AI to optimize the schedule if available
        ai_sessions = _optimize_schedule_with_ai(modules, calendar_events, preferences, previous_feedback)
        
        if ai_sessions:
            # AI optimization successful
            return [StudySession(**session) for session in ai_sessions]
        
        # Fallback to heuristic scheduling
        logger.info("Falling back to heuristic scheduling")
        
        # Calculate available time slots based on preferences
        time_slots = _calculate_time_slots(preferences)
        
        # Filter out unavailable slots based on calendar and excluded times
        available_slots = _filter_available_slots(
            time_slots, 
            calendar_events, 
            preferences.excluded_times
        )
        
        # Distribute modules across available slots
        study_sessions = _distribute_modules_to_slots(
            available_slots,
            modules,
            preferences
        )
        
        # Return the generated sessions
        return [StudySession(**session) for session in study_sessions]
        
    except Exception as e:
        logger.error(f"Error generating study schedule: {str(e)}")
        return []

def save_study_sessions(sessions: List[StudySession]) -> List[Dict[str, Any]]:
    """
    Save study sessions to the database.
    
    Args:
        sessions: List of study sessions to save
        
    Returns:
        The saved sessions with their IDs
    """
    saved_sessions = []
    
    # Use the same batch ID for all sessions in this set
    batch_id = str(uuid.uuid4())
    
    for session in sessions:
        try:
            # Generate ID if not present
            if not session.id:
                session.id = str(uuid.uuid4())
            
            # Set batch ID if not present
            if not session.batch_id:
                session.batch_id = batch_id
            
            # Add type for database
            session_dict = session.dict()
            session_dict["type"] = "study_session"
            
            # Create session in database
            created_session = _container.create_item(body=session_dict)
            saved_sessions.append(created_session)
            
        except Exception as e:
            logger.error(f"Error saving study session: {str(e)}")
    
    return saved_sessions

def create_calendar_events_from_sessions(sessions: List[StudySession]) -> List[Dict[str, Any]]:
    """
    Create calendar events from study sessions.
    
    Args:
        sessions: List of study sessions
        
    Returns:
        List of created calendar events
    """
    from calendar_routes import create_event  # Local import to avoid circular dependencies
    
    created_events = []
    
    for session in sessions:
        try:
            # Create event data
            event_data = {
                "title": session.title,
                "description": session.description,
                "date": session.date,
                "all_day": False,
                "start_time": session.start_time,
                "end_time": session.end_time,
                "type": "study",  # Custom event type for study sessions
                "user_email": session.user_email,
                "metadata": {
                    "study_session_id": session.id,
                    "module_id": session.module_id,
                    "is_ai_generated": session.is_ai_generated
                }
            }
            
            # Create mock request object
            from types import SimpleNamespace
            req = SimpleNamespace()
            req.get_json = lambda: event_data
            req.headers = {"Authorization": "Bearer dummy"}  # This will be ignored as we pass user_email directly
            
            # Use our existing calendar API
            response = create_event(req, user_email=session.user_email)
            
            # Check if successful
            if hasattr(response, 'status_code') and response.status_code == 201:
                # Extract created event data
                event = json.loads(response.get_body().decode('utf-8'))
                
                # Update session with event ID
                session_dict = session.dict()
                session_dict["calendar_event_id"] = event["id"]
                
                # Update session in database
                _container.upsert_item(body=session_dict)
                
                created_events.append(event)
            
        except Exception as e:
            logger.error(f"Error creating calendar event: {str(e)}")
    
    return created_events

def update_session_status(session_id: str, status: str, feedback: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Update a study session's status and optionally add feedback.
    
    Args:
        session_id: ID of the session to update
        status: New status (completed, missed, rescheduled)
        feedback: Optional feedback dictionary
        
    Returns:
        The updated session
    """
    try:
        # Get the session
        query = f"SELECT * FROM c WHERE c.id = '{session_id}' AND c.type = 'study_session'"
        sessions = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if not sessions:
            logger.error(f"Session not found: {session_id}")
            return None
        
        session = sessions[0]
        
        # Update status
        session["status"] = status
        
        # Add feedback if provided
        if feedback:
            session["feedback"] = feedback
        
        # Update session in database
        updated_session = _container.upsert_item(body=session)
        
        return updated_session
        
    except Exception as e:
        logger.error(f"Error updating session status: {str(e)}")
        return None

def get_recommendations_based_on_feedback(user_email: str) -> Dict[str, Any]:
    """
    Generate recommendations based on user's session feedback.
    
    Args:
        user_email: The user's email
        
    Returns:
        Dictionary with recommendations
    """
    try:
        # Get completed sessions with feedback
        query = f"""
        SELECT * FROM c 
        WHERE c.type = 'study_session' 
        AND c.user_email = '{user_email}'
        AND c.status = 'completed'
        AND IS_DEFINED(c.feedback)
        """
        
        sessions = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if not sessions:
            return {
                "enough_data": False,
                "message": "Not enough data to generate recommendations."
            }
        
        # Analyze feedback
        module_performance = {}
        time_performance = {}
        
        for session in sessions:
            feedback = session.get("feedback", {})
            
            # Skip sessions without meaningful feedback
            if not feedback or "productivity_rating" not in feedback:
                continue
            
            # Track module performance
            module_id = session.get("module_id")
            if module_id:
                if module_id not in module_performance:
                    module_performance[module_id] = {
                        "total_rating": 0,
                        "count": 0,
                        "module_name": session.get("module_name", "Unknown Module")
                    }
                
                module_performance[module_id]["total_rating"] += feedback.get("productivity_rating", 3)
                module_performance[module_id]["count"] += 1
            
            # Track time of day performance
            start_time = session.get("start_time")
            if start_time:
                try:
                    hour = int(start_time.split(":")[0])
                    
                    time_of_day = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening" if hour < 21 else "night"
                    
                    if time_of_day not in time_performance:
                        time_performance[time_of_day] = {
                            "total_rating": 0,
                            "count": 0
                        }
                    
                    time_performance[time_of_day]["total_rating"] += feedback.get("productivity_rating", 3)
                    time_performance[time_of_day]["count"] += 1
                    
                except:
                    pass
        
        # Calculate averages
        for module_id in module_performance:
            data = module_performance[module_id]
            data["average_rating"] = round(data["total_rating"] / data["count"], 1) if data["count"] > 0 else 0
        
        for time in time_performance:
            data = time_performance[time]
            data["average_rating"] = round(data["total_rating"] / data["count"], 1) if data["count"] > 0 else 0
        
        # Generate recommendations
        recommendations = {
            "enough_data": True,
            "message": "Based on your study feedback, we have the following recommendations:",
            "best_modules": [],
            "challenging_modules": [],
            "best_times": [],
            "adjustments": []
        }
        
        # Best and most challenging modules
        if module_performance:
            sorted_modules = sorted(
                [(module_id, data) for module_id, data in module_performance.items()],
                key=lambda x: x[1]["average_rating"],
                reverse=True
            )
            
            # Best modules
            for module_id, data in sorted_modules[:2]:
                if data["average_rating"] >= 3.5:
                    recommendations["best_modules"].append({
                        "module_id": module_id,
                        "module_name": data["module_name"],
                        "average_rating": data["average_rating"]
                    })
            
            # Challenging modules
            for module_id, data in sorted_modules[-2:]:
                if data["average_rating"] <= 3.0:
                    recommendations["challenging_modules"].append({
                        "module_id": module_id,
                        "module_name": data["module_name"],
                        "average_rating": data["average_rating"]
                    })
        
        # Best times
        if time_performance:
            sorted_times = sorted(
                [(time, data) for time, data in time_performance.items()],
                key=lambda x: x[1]["average_rating"],
                reverse=True
            )
            
            for time, data in sorted_times[:2]:
                if data["average_rating"] >= 3.0:
                    recommendations["best_times"].append({
                        "time_of_day": time,
                        "average_rating": data["average_rating"]
                    })
        
        # Generate adjustment recommendations
        user_preferences = get_user_study_preference(user_email)
        
        # Suggest optimal study times
        if recommendations["best_times"]:
            optimal_times = [t["time_of_day"] for t in recommendations["best_times"]]
            
            if not all(time in user_preferences.preferred_times for time in optimal_times):
                missing_times = [time for time in optimal_times if time not in user_preferences.preferred_times]
                
                if missing_times:
                    recommendations["adjustments"].append({
                        "type": "preferred_times",
                        "message": f"Consider adding {', '.join(missing_times)} to your preferred study times based on your past performance."
                    })
        
        # Suggest session duration adjustments
        productivity_sum = sum(s.get("feedback", {}).get("productivity_rating", 0) for s in sessions if "feedback" in s)
        productivity_count = sum(1 for s in sessions if "feedback" in s and "productivity_rating" in s.get("feedback", {}))
        
        avg_productivity = productivity_sum / productivity_count if productivity_count > 0 else 0
        
        if avg_productivity < 3.0 and user_preferences.study_session_duration > 45:
            recommendations["adjustments"].append({
                "type": "session_duration",
                "message": f"Consider shortening your study sessions. Your current setting is {user_preferences.study_session_duration} minutes, but shorter sessions (45 mins) might help improve focus."
            })
        elif avg_productivity >= 4.0 and user_preferences.study_session_duration < 75:
            recommendations["adjustments"].append({
                "type": "session_duration", 
                "message": f"You seem to maintain good focus. Consider increasing your study sessions from {user_preferences.study_session_duration} to 75-90 minutes to maximize productivity."
            })
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        return {
            "enough_data": False,
            "message": f"Error generating recommendations: {str(e)}"
        }