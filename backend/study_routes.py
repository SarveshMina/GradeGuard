# study_routes.py
import json
import traceback
import azure.functions as func
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from user_routes import verify_session
from database import get_user_by_email
from study_database import (
    get_study_preferences,
    save_study_preferences,
    get_module_study_preferences,
    save_module_study_preference,
    get_study_sessions,
    save_study_session,
    update_session_status,
    get_study_streak,
    get_achievements,
    create_default_achievements,
    get_study_stats,
    update_study_stats
)
from ai_service import (
    generate_study_schedule,
    suggest_study_topics
)
from calendar_integration import (
    parse_ical_url,
    import_ical_events,
    store_ical_subscription,
    get_user_ical_subscriptions,
    sync_ical_subscription,
    delete_ical_subscription
)
from models import (
    StudyPreferences,
    ModuleStudyPreference,
    StudySession,
    StudySessionStatus,
    OpenAIScheduleRequest
)

# Study Preferences Routes
def get_user_study_preferences(req: func.HttpRequest) -> func.HttpResponse:
    """Get study preferences for the authenticated user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get preferences from database
        preferences = get_study_preferences(identity)
        
        if not preferences:
            # Return default preferences if none exist
            default_prefs = {
                "preferred_times": ["morning", "afternoon"],
                "available_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "session_duration": 60,
                "break_duration": 15,
                "max_sessions_per_day": 3,
                "environment_preference": "quiet",
                "focus_levels": {
                    "morning": 8,
                    "afternoon": 6,
                    "evening": 7,
                    "night": 4
                }
            }
            return func.HttpResponse(json.dumps(default_prefs), status_code=200)
        
        # Return preferences without metadata fields
        cleaned_prefs = {k: v for k, v in preferences.items() if k not in ["id", "type", "user_email"]}
        return func.HttpResponse(json.dumps(cleaned_prefs), status_code=200)
    
    except Exception as e:
        print(f"Error getting study preferences: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_study_preferences(req: func.HttpRequest) -> func.HttpResponse:
    """Update study preferences for the authenticated user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get the request data
        req_body = req.get_json()
        
        # Add user email to the data
        req_body["user_email"] = identity
        
        # Validate with Pydantic model
        preferences = StudyPreferences(**req_body)
        
        # Save to database
        result = save_study_preferences(preferences)
        
        # Return success response
        return func.HttpResponse(json.dumps({"message": "Study preferences updated successfully"}), status_code=200)
    
    except Exception as e:
        print(f"Error updating study preferences: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

# Module Preferences Routes
def get_module_preferences(req: func.HttpRequest) -> func.HttpResponse:
    """Get module study preferences for the authenticated user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Check for module_id in query parameters
        module_id = req.params.get('module_id')
        
        # Get preferences from database
        preferences = get_module_study_preferences(identity, module_id)
        
        # Return an empty list if no preferences exist
        if not preferences:
            if module_id:
                # Return default for specific module
                return func.HttpResponse(json.dumps({
                    "module_id": module_id,
                    "priority": 3,
                    "weekly_hours_goal": 3.0,
                    "difficulty_rating": 3
                }), status_code=200)
            else:
                # Return empty list
                return func.HttpResponse(json.dumps([]), status_code=200)
        
        # Return single preference or list depending on the request
        if module_id:
            # Return single preference without metadata fields
            cleaned_pref = {k: v for k, v in preferences[0].items() if k not in ["id", "type", "user_email"]}
            return func.HttpResponse(json.dumps(cleaned_pref), status_code=200)
        else:
            # Return list of preferences without metadata fields
            cleaned_prefs = [{k: v for k, v in pref.items() if k not in ["id", "type", "user_email"]} for pref in preferences]
            return func.HttpResponse(json.dumps(cleaned_prefs), status_code=200)
    
    except Exception as e:
        print(f"Error getting module preferences: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_module_preference(req: func.HttpRequest) -> func.HttpResponse:
    """Update module study preference for the authenticated user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get the request data
        req_body = req.get_json()
        
        # Validate with Pydantic model
        preference = ModuleStudyPreference(**req_body)
        
        # Save to database
        result = save_module_study_preference(preference, identity)
        
        # Return success response
        return func.HttpResponse(json.dumps({"message": "Module preference updated successfully"}), status_code=200)
    
    except Exception as e:
        print(f"Error updating module preference: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

# Study Sessions Routes
def get_user_study_sessions(req: func.HttpRequest) -> func.HttpResponse:
    """Get study sessions for the authenticated user with optional filters"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get query parameters
        start_date = req.params.get('start_date')
        end_date = req.params.get('end_date')
        status = req.params.get('status')
        module_id = req.params.get('module_id')
        
        # If no start date provided, default to today
        if not start_date:
            start_date = datetime.utcnow().date().isoformat()
        
        # If no end date provided, default to 7 days from start
        if not end_date:
            start_date_obj = datetime.fromisoformat(start_date)
            end_date = (start_date_obj + timedelta(days=7)).isoformat()
        
        # Get sessions from database
        sessions = get_study_sessions(identity, start_date, end_date, status, module_id)
        
        # Return sessions without sensitive fields
        cleaned_sessions = [{k: v for k, v in session.items() if k not in ["type", "user_email"]} for session in sessions]
        return func.HttpResponse(json.dumps(cleaned_sessions), status_code=200)
    
    except Exception as e:
        print(f"Error getting study sessions: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_study_session(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new study session"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get the request data
        req_body = req.get_json()
        
        # Add user email to the data
        req_body["user_email"] = identity
        
        # Validate with Pydantic model
        session = StudySession(**req_body)
        
        # Save to database
        result = save_study_session(session)
        
        # Return the created session without sensitive fields
        cleaned_result = {k: v for k, v in result.items() if k not in ["type", "user_email"]}
        return func.HttpResponse(json.dumps(cleaned_result), status_code=201)
    
    except Exception as e:
        print(f"Error creating study session: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def update_study_session(req: func.HttpRequest) -> func.HttpResponse:
    """Update an existing study session"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get session ID from route
        session_id = req.route_params.get('id')
        if not session_id:
            return func.HttpResponse(json.dumps({"error": "Session ID is required"}), status_code=400)
        
        # Get the request data
        req_body = req.get_json()
        
        # Add required fields
        req_body["id"] = session_id
        req_body["user_email"] = identity
        
        # Validate with Pydantic model
        session = StudySession(**req_body)
        
        # Save to database
        result = save_study_session(session)
        
        # Return the updated session without sensitive fields
        cleaned_result = {k: v for k, v in result.items() if k not in ["type", "user_email"]}
        return func.HttpResponse(json.dumps(cleaned_result), status_code=200)
    
    except Exception as e:
        print(f"Error updating study session: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def update_session_status_route(req: func.HttpRequest) -> func.HttpResponse:
    """Update a study session's status with optional feedback"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get session ID from route
        session_id = req.route_params.get('id')
        if not session_id:
            return func.HttpResponse(json.dumps({"error": "Session ID is required"}), status_code=400)
        
        # Get the request data
        req_body = req.get_json()
        
        # Extract fields
        status = req_body.get("status")
        if not status:
            return func.HttpResponse(json.dumps({"error": "Status is required"}), status_code=400)
        
        productivity_rating = req_body.get("productivity_rating")
        difficulty_rating = req_body.get("difficulty_rating")
        notes = req_body.get("notes")
        
        # Update in database
        result = update_session_status(
            session_id, 
            status,
            productivity_rating,
            difficulty_rating,
            notes
        )
        
        # Return success with points earned if completed
        response = {"message": f"Session status updated to {status}"}
        if status == "completed" and "points_earned" in result:
            response["points_earned"] = result["points_earned"]
        
        return func.HttpResponse(json.dumps(response), status_code=200)
    
    except Exception as e:
        print(f"Error updating session status: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

# Schedule Generation Route
def generate_schedule(req: func.HttpRequest) -> func.HttpResponse:
    """Generate an AI-powered study schedule"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get the request data
        req_body = req.get_json()
        
        # Extract schedule parameters
        start_date = req_body.get("start_date")
        if not start_date:
            # Default to today
            start_date = datetime.utcnow().date().isoformat()
            
        end_date = req_body.get("end_date")
        if not end_date:
            # Default to 7 days from start
            start_date_obj = datetime.fromisoformat(start_date)
            end_date = (start_date_obj + timedelta(days=7)).isoformat()
        
        module_ids = req_body.get("module_ids", [])
        if not module_ids:
            return func.HttpResponse(json.dumps({"error": "At least one module ID is required"}), status_code=400)
        
        # Get study preferences
        preferences = get_study_preferences(identity)
        if not preferences:
            return func.HttpResponse(json.dumps({"error": "Study preferences must be set before generating a schedule"}), status_code=400)
        
        # Get module preferences
        module_preferences = []
        for module_id in module_ids:
            module_prefs = get_module_study_preferences(identity, module_id)
            if module_prefs:
                module_preferences.append(module_prefs[0])
            else:
                # Create default preference
                default_pref = {
                    "module_id": module_id,
                    "priority": 3,
                    "weekly_hours_goal": 3.0,
                    "difficulty_rating": 3
                }
                module_preferences.append(default_pref)
        
        # Get existing calendar events
        from calendar_routes import get_events
        
        # Create mock request for get_events
        class MockHttpRequest:
            def __init__(self, params):
                self.params = params
                
            def get_json(self):
                return {}
        
        mock_params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        mock_req = MockHttpRequest(mock_params)
        calendar_response = get_events(mock_req)
        calendar_events = json.loads(calendar_response.get_body().decode('utf-8'))
        
        # Create request object for AI service
        schedule_request = OpenAIScheduleRequest(
            user_email=identity,
            study_preferences=StudyPreferences(**preferences),
            module_preferences=[ModuleStudyPreference(**pref) for pref in module_preferences],
            existing_events=calendar_events,
            start_date=start_date,
            end_date=end_date
        )
        
        # Call AI service to generate schedule
        schedule_response = generate_study_schedule(schedule_request)
        
        # Save the generated study sessions
        saved_sessions = []
        for session in schedule_response.study_sessions:
            result = save_study_session(session)
            saved_sessions.append(result)
        
        # Return the generated schedule
        response = {
            "sessions": saved_sessions,
            "total_study_hours": schedule_response.total_study_hours,
            "module_distribution": schedule_response.module_distribution,
            "recommendations": schedule_response.recommendations
        }
        
        return func.HttpResponse(json.dumps(response), status_code=200)
    
    except Exception as e:
        print(f"Error generating study schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# Calendar Integration Routes
def import_ical_calendar(req: func.HttpRequest) -> func.HttpResponse:
    """Import events from an iCal feed"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get the request data
        req_body = req.get_json()
        
        # Extract iCal URL
        ical_url = req_body.get("ical_url")
        if not ical_url:
            return func.HttpResponse(json.dumps({"error": "iCal URL is required"}), status_code=400)
        
        # Extract optional name for the subscription
        name = req_body.get("name", "Calendar Subscription")
        
        # Extract save option
        save_subscription = req_body.get("save_subscription", True)
        
        # Import events
        results = import_ical_events(ical_url, identity)
        
        # Save subscription if requested
        if save_subscription:
            subscription = store_ical_subscription(identity, ical_url, name)
            results["subscription"] = subscription
        
        return func.HttpResponse(json.dumps(results), status_code=200)
    
    except Exception as e:
        print(f"Error importing iCal calendar: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_ical_subscriptions(req: func.HttpRequest) -> func.HttpResponse:
    """Get all iCal subscriptions for the user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get subscriptions
        subscriptions = get_user_ical_subscriptions(identity)
        
        # Clean the output
        cleaned_subs = []
        for sub in subscriptions:
            cleaned_sub = {
                "id": sub["id"],
                "name": sub["name"],
                "ical_url": sub["ical_url"],
                "last_sync": sub["last_sync"],
                "created_at": sub["created_at"],
                "auto_sync": sub.get("auto_sync", True)
            }
            cleaned_subs.append(cleaned_sub)
        
        return func.HttpResponse(json.dumps(cleaned_subs), status_code=200)
    
    except Exception as e:
        print(f"Error getting iCal subscriptions: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def sync_ical_subscription_route(req: func.HttpRequest) -> func.HttpResponse:
    """Sync events from an iCal subscription"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get subscription ID from route
        subscription_id = req.route_params.get('id')
        if not subscription_id:
            return func.HttpResponse(json.dumps({"error": "Subscription ID is required"}), status_code=400)
        
        # Sync the subscription
        results = sync_ical_subscription(subscription_id)
        
        return func.HttpResponse(json.dumps(results), status_code=200)
    
    except Exception as e:
        print(f"Error syncing iCal subscription: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def delete_ical_subscription_route(req: func.HttpRequest) -> func.HttpResponse:
    """Delete an iCal subscription"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get subscription ID from route
        subscription_id = req.route_params.get('id')
        if not subscription_id:
            return func.HttpResponse(json.dumps({"error": "Subscription ID is required"}), status_code=400)
        
        # Check if events should be deleted
        delete_events = req.params.get('delete_events', 'false').lower() == 'true'
        
        # Delete the subscription
        results = delete_ical_subscription(subscription_id, identity, delete_events)
        
        return func.HttpResponse(json.dumps(results), status_code=200)
    
    except Exception as e:
        print(f"Error deleting iCal subscription: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# Achievements and Gamification Routes
def get_user_streak(req: func.HttpRequest) -> func.HttpResponse:
    """Get the user's current study streak"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get streak information
        streak = get_study_streak(identity)
        
        # Clean the output
        cleaned_streak = {
            "current_streak": streak["current_streak"],
            "longest_streak": streak["longest_streak"],
            "last_study_date": streak["last_study_date"]
        }
        
        return func.HttpResponse(json.dumps(cleaned_streak), status_code=200)
    
    except Exception as e:
        print(f"Error getting user streak: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_user_achievements(req: func.HttpRequest) -> func.HttpResponse:
    """Get all achievements for the user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Check for category filter
        category = req.params.get('category')
        
        # Get achievements
        achievements = get_achievements(identity, category)
        
        # If no achievements, create defaults
        if not achievements:
            create_default_achievements(identity)
            # Get the newly created achievements
            achievements = get_achievements(identity, category)
        
        # Clean the output
        cleaned_achievements = []
        for ach in achievements:
            cleaned_ach = {
                "id": ach["id"],
                "name": ach["name"],
                "description": ach["description"],
                "status": ach["status"],
                "progress": ach["progress"],
                "target": ach["target"],
                "progress_percent": ach.get("progress_percent", int((ach["progress"] / ach["target"]) * 100)),
                "unlocked_date": ach.get("unlocked_date"),
                "completed_date": ach.get("completed_date"),
                "badge_icon": ach.get("badge_icon"),
                "category": ach["category"]
            }
            cleaned_achievements.append(cleaned_ach)
        
        # Group by category if no specific category was requested
        if not category:
            by_category = {}
            for ach in cleaned_achievements:
                cat = ach["category"]
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(ach)
            
            return func.HttpResponse(json.dumps(by_category), status_code=200)
        
        return func.HttpResponse(json.dumps(cleaned_achievements), status_code=200)
    
    except Exception as e:
        print(f"Error getting user achievements: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_user_study_stats_route(req: func.HttpRequest) -> func.HttpResponse:
    """Get study statistics for the user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get stats
        stats = get_study_stats(identity)
        
        # Clean the output
        cleaned_stats = {
            "total_sessions_planned": stats["total_sessions_planned"],
            "total_sessions_completed": stats["total_sessions_completed"],
            "completion_rate": round(stats["total_sessions_completed"] / max(1, stats["total_sessions_planned"]) * 100, 1),
            "total_study_time_minutes": stats["total_study_time_minutes"],
            "total_study_hours": round(stats["total_study_time_minutes"] / 60, 1),
            "avg_productivity_rating": stats["avg_productivity_rating"],
            "most_studied_module": stats["most_studied_module"],
            "level": stats["level"],
            "total_xp": stats["total_xp"],
            "modules_stats": stats.get("modules_stats", {})
        }
        
        # Calculate XP required for next level
        level_thresholds = [
            0, 1000, 2500, 5000, 10000, 17500, 27500, 40000, 55000, 75000, 
            100000, 130000, 165000, 205000, 250000, 300000, 355000, 415000, 480000, 550000
        ]
        
        current_level = stats["level"]
        if current_level < len(level_thresholds):
            next_level_xp = level_thresholds[current_level]
            cleaned_stats["next_level_xp"] = next_level_xp
            cleaned_stats["xp_for_next_level"] = next_level_xp - stats["total_xp"]
            cleaned_stats["level_progress_percent"] = min(100, int((stats["total_xp"] / next_level_xp) * 100))
        
        return func.HttpResponse(json.dumps(cleaned_stats), status_code=200)
    
    except Exception as e:
        print(f"Error getting user study stats: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def refresh_study_stats(req: func.HttpRequest) -> func.HttpResponse:
    """Manually refresh study statistics"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Update stats
        stats = update_study_stats(identity)
        
        return func.HttpResponse(json.dumps({"message": "Study statistics updated successfully"}), status_code=200)
    
    except Exception as e:
        print(f"Error refreshing study stats: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# Topic Suggestions
def get_study_topic_suggestions(req: func.HttpRequest) -> func.HttpResponse:
    """Get AI-suggested topics for a study session"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get query parameters
        module_id = req.params.get('module_id')
        if not module_id:
            return func.HttpResponse(json.dumps({"error": "Module ID is required"}), status_code=400)
        
        # Get module preferences for topics
        module_prefs = get_module_study_preferences(identity, module_id)
        if not module_prefs:
            return func.HttpResponse(json.dumps({"error": "Module preferences not found"}), status_code=404)
        
        # Get topics from preferences
        topics = module_prefs[0].get("topics", [])
        if not topics:
            return func.HttpResponse(json.dumps({"error": "Module has no topics defined"}), status_code=400)
        
        # Get assessment date if available
        assessment_date = None
        assessment_dates = module_prefs[0].get("assessment_dates", [])
        if assessment_dates:
            # Use nearest assessment date
            today = datetime.utcnow()
            nearest_date = None
            nearest_diff = float('inf')
            
            for date_str in assessment_dates:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                diff = (date - today).total_seconds()
                if diff > 0 and diff < nearest_diff:
                    nearest_diff = diff
                    nearest_date = date_str
            
            assessment_date = nearest_date
        
        # Get suggestions
        suggestions = suggest_study_topics(module_id, topics, assessment_date)
        
        return func.HttpResponse(json.dumps(suggestions), status_code=200)
    
    except Exception as e:
        print(f"Error getting study topic suggestions: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)