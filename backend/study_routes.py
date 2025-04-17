# study_routes.py
import azure.functions as func
import json
import traceback
import datetime
import uuid
from typing import List, Dict, Any, Optional
from user_routes import verify_session
from models import ScheduleRequest, FeedbackForm, StudySessionStatus
from study_database import (
    create_study_schedule, get_user_schedules, get_schedule, update_schedule, delete_schedule,
    create_study_session, get_user_sessions, get_session, update_session, delete_session,
    delete_sessions_for_schedule, get_active_schedule, activate_schedule, mark_schedule_events_created,
    get_active_schedule_sessions, deactivate_all_schedules,
    get_study_streak, update_study_streak,
    get_user_achievements, check_and_update_achievements,
    get_study_stats, update_study_stats,
    create_ai_tip, get_user_ai_tips, update_ai_tip_status,
    get_module_study_stats, get_module_time_distribution, get_sessions_timeline, get_productivity_patterns,
    get_grade_distribution_data
)
from ai_scheduler import generate_study_schedule, generate_ai_tips
from calendar_routes import create_event
from database import get_user_modules

# === Schedule Routes ===

def get_schedules(req: func.HttpRequest) -> func.HttpResponse:
    """Get all study schedules for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        schedules = get_user_schedules(identity)
        return func.HttpResponse(json.dumps(schedules), status_code=200)
    except Exception as e:
        print(f"Error getting schedules: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_active_schedule_route(req: func.HttpRequest) -> func.HttpResponse:
    """Get the currently active study schedule for the user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        active_schedule = get_active_schedule(identity)
        if not active_schedule:
            return func.HttpResponse(json.dumps({"message": "No active schedule found"}), status_code=404)
            
        return func.HttpResponse(json.dumps(active_schedule), status_code=200)
    except Exception as e:
        print(f"Error getting active schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_schedule_manual(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new study schedule manually"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Parse request
        schedule_data = req.get_json()

        # Validate with model
        try:
            schedule_request = ScheduleRequest(**schedule_data)
        except Exception as e:
            return func.HttpResponse(
                json.dumps({"error": f"Validation error: {str(e)}"}),
                status_code=400
            )

        # Create schedule document
        schedule_doc = {
            "name": schedule_request.name,
            "start_date": schedule_request.start_date,
            "end_date": schedule_request.end_date,
            "preferred_times": schedule_request.preferred_times,
            "available_days": schedule_request.available_days,
            "session_duration": schedule_request.session_duration,
            "break_duration": schedule_request.break_duration,
            "max_sessions_per_day": schedule_request.max_sessions_per_day,
            "modules": schedule_request.modules,
            "is_ai_generated": False,
            "is_active": schedule_data.get("is_active", True),  # Default to active if not specified
            "events_created": False  # Flag to track if events have been created
        }

        # Save schedule to database
        created_schedule = create_study_schedule(identity, schedule_doc)

        # Generate study sessions from the schedule, but don't create calendar events yet
        sessions = create_sessions_from_schedule(identity, created_schedule, create_calendar_events=False)

        return func.HttpResponse(
            json.dumps({
                "schedule": created_schedule,
                "sessions": sessions,
                "message": "Schedule created successfully. Confirm to add events to calendar."
            }),
            status_code=201
        )
    except Exception as e:
        print(f"Error creating schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_schedule_ai(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new study schedule using AI"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Parse request
        schedule_data = req.get_json()

        # Validate with model
        try:
            schedule_request = ScheduleRequest(**schedule_data)
        except Exception as e:
            return func.HttpResponse(
                json.dumps({"error": f"Validation error: {str(e)}"}),
                status_code=400
            )

        # Get module details for AI
        modules_info = []
        for module_id in schedule_request.modules:
            # Get module info from your modules database
            module = get_module_by_id(identity, module_id)
            if module:
                modules_info.append(module)

        # Generate AI-powered schedule
        ai_schedule, study_sessions = generate_study_schedule(
            identity,
            schedule_request.dict(),
            modules_info
        )

        # Save AI-generated schedule
        ai_schedule["is_ai_generated"] = True
        ai_schedule["is_active"] = schedule_data.get("is_active", True)  # Default to active if not specified
        ai_schedule["events_created"] = False  # Flag to track if events have been created
        created_schedule = create_study_schedule(identity, ai_schedule)

        # Save generated sessions without creating calendar events yet
        sessions = []
        for session_data in study_sessions:
            session_data["schedule_id"] = created_schedule["id"]
            created_session = create_study_session(identity, session_data)
            sessions.append(created_session)

        return func.HttpResponse(
            json.dumps({
                "schedule": created_schedule,
                "sessions": sessions,
                "message": "AI schedule generated successfully. Confirm to add events to calendar."
            }),
            status_code=201
        )
    except Exception as e:
        print(f"Error creating AI schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_schedule_route(req: func.HttpRequest) -> func.HttpResponse:
    """Update an existing schedule"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    schedule_id = req.route_params.get('id')
    if not schedule_id:
        return func.HttpResponse(json.dumps({"error": "Schedule ID is required"}), status_code=400)

    try:
        update_data = req.get_json()
        updated_schedule = update_schedule(identity, schedule_id, update_data)

        if not updated_schedule:
            return func.HttpResponse(
                json.dumps({"error": "Schedule not found or access denied"}),
                status_code=404
            )

        return func.HttpResponse(json.dumps(updated_schedule), status_code=200)
    except Exception as e:
        print(f"Error updating schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def delete_schedule_route(req: func.HttpRequest) -> func.HttpResponse:
    """Delete a schedule and all its associated sessions"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    schedule_id = req.route_params.get('id')
    if not schedule_id:
        return func.HttpResponse(json.dumps({"error": "Schedule ID is required"}), status_code=400)

    try:
        # Get the schedule first to check if it exists
        schedule = get_schedule(identity, schedule_id)
        if not schedule:
            return func.HttpResponse(
                json.dumps({"error": "Schedule not found or access denied"}),
                status_code=404
            )
            
        # Delete associated sessions first
        deleted_session_count = delete_sessions_for_schedule(identity, schedule_id)
        
        # Delete calendar events if they exist (based on session event_id references)
        # This functionality would depend on your calendar_routes implementation
        
        # Then delete the schedule
        success = delete_schedule(identity, schedule_id)

        if not success:
            return func.HttpResponse(
                json.dumps({"error": "Failed to delete schedule"}),
                status_code=500
            )

        return func.HttpResponse(
            json.dumps({
                "message": "Schedule and associated sessions deleted", 
                "deleted_sessions": deleted_session_count
            }),
            status_code=200
        )
    except Exception as e:
        print(f"Error deleting schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def activate_schedule_route(req: func.HttpRequest) -> func.HttpResponse:
    """Activate a specific schedule and deactivate all others"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    schedule_id = req.route_params.get('id')
    if not schedule_id:
        return func.HttpResponse(json.dumps({"error": "Schedule ID is required"}), status_code=400)

    try:
        # Activate the schedule
        updated_schedule = activate_schedule(identity, schedule_id)

        if not updated_schedule:
            return func.HttpResponse(
                json.dumps({"error": "Schedule not found or access denied"}),
                status_code=404
            )

        return func.HttpResponse(
            json.dumps({
                "message": "Schedule activated successfully",
                "schedule": updated_schedule
            }),
            status_code=200
        )
    except Exception as e:
        print(f"Error activating schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_calendar_events_route(req: func.HttpRequest) -> func.HttpResponse:
    """Create calendar events for a schedule after user confirmation"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    schedule_id = req.route_params.get('id')
    if not schedule_id:
        return func.HttpResponse(json.dumps({"error": "Schedule ID is required"}), status_code=400)

    try:
        # Get the schedule
        schedule = get_schedule(identity, schedule_id)
        if not schedule:
            return func.HttpResponse(
                json.dumps({"error": "Schedule not found or access denied"}),
                status_code=404
            )
            
        # Check if events are already created
        if schedule.get("events_created", False):
            return func.HttpResponse(
                json.dumps({"message": "Calendar events already created for this schedule"}),
                status_code=200
            )
            
        # Get all sessions for this schedule
        sessions = get_user_sessions(identity, schedule_id=schedule_id)
        
        # Create calendar events for each session
        created_events = []
        for session in sessions:
            event_id = create_calendar_event_for_session(req, identity, session)
            if event_id:
                # Update session with event_id
                update_session(identity, session["id"], {"event_id": event_id})
                created_events.append(event_id)
                
        # Mark schedule as having events created
        mark_schedule_events_created(identity, schedule_id)
        
        return func.HttpResponse(
            json.dumps({
                "message": f"Successfully created {len(created_events)} calendar events",
                "created_events": len(created_events)
            }),
            status_code=200
        )
    except Exception as e:
        print(f"Error creating calendar events: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# === Study Session Routes ===

def get_sessions(req: func.HttpRequest) -> func.HttpResponse:
    """Get study sessions for the current user, filtered by active schedule if requested"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get optional date range filters
        start_date = req.params.get('start_date')
        end_date = req.params.get('end_date')
        
        # Check if we should filter by active schedule only
        active_only = req.params.get('active_only', 'false').lower() == 'true'
        
        if active_only:
            # Get sessions only from active schedule
            sessions = get_active_schedule_sessions(identity, start_date, end_date)
        else:
            # Get optional schedule_id filter
            schedule_id = req.params.get('schedule_id')
            
            # Get all sessions (potentially filtered by schedule_id)
            sessions = get_user_sessions(identity, start_date, end_date, schedule_id)
            
        return func.HttpResponse(json.dumps(sessions), status_code=200)
    except Exception as e:
        print(f"Error getting sessions: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def start_session(req: func.HttpRequest) -> func.HttpResponse:
    """Start a study session"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    session_id = req.route_params.get('id')
    if not session_id:
        return func.HttpResponse(json.dumps({"error": "Session ID is required"}), status_code=400)

    try:
        # Get the session
        session = get_session(identity, session_id)
        if not session:
            return func.HttpResponse(
                json.dumps({"error": "Session not found or access denied"}),
                status_code=404
            )

        # Update status to in_progress
        updates = {
            "status": "in_progress",
            "started_at": datetime.datetime.utcnow().isoformat()
        }

        updated_session = update_session(identity, session_id, updates)

        return func.HttpResponse(json.dumps(updated_session), status_code=200)
    except Exception as e:
        print(f"Error starting session: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def complete_session(req: func.HttpRequest) -> func.HttpResponse:
    """Complete a study session with feedback"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    session_id = req.route_params.get('id')
    if not session_id:
        return func.HttpResponse(json.dumps({"error": "Session ID is required"}), status_code=400)

    try:
        # Get feedback data
        feedback_data = req.get_json()

        # Validate with model
        try:
            feedback = FeedbackForm(**feedback_data)
        except Exception as e:
            return func.HttpResponse(
                json.dumps({"error": f"Validation error: {str(e)}"}),
                status_code=400
            )

        # Get the session
        session = get_session(identity, session_id)
        if not session:
            return func.HttpResponse(
                json.dumps({"error": "Session not found or access denied"}),
                status_code=404
            )

        # Calculate XP based on productivity and session duration
        productivity = feedback.productivity
        xp_earned = calculate_xp(session, productivity)

        # Update session with completion data
        updates = {
            "status": "completed",
            "completed": True,
            "completed_at": datetime.datetime.utcnow().isoformat(),
            "productivity": productivity,
            "difficulty": feedback.difficulty,
            "notes": feedback.notes,
            "topics": feedback.topics,
            "xpEarned": xp_earned
        }

        updated_session = update_session(identity, session_id, updates)

        # Update study streak
        current_date = datetime.datetime.utcnow().date().isoformat()
        update_study_streak(identity, current_date, True)

        # Update achievements
        check_and_update_achievements(identity)

        # Update study stats
        update_study_stats(identity)

        # Generate AI tips based on new data
        generate_user_tips(identity)

        return func.HttpResponse(json.dumps(updated_session), status_code=200)
    except Exception as e:
        print(f"Error completing session: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def reschedule_session(req: func.HttpRequest) -> func.HttpResponse:
    """Reschedule a study session"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    session_id = req.route_params.get('id')
    if not session_id:
        return func.HttpResponse(json.dumps({"error": "Session ID is required"}), status_code=400)

    try:
        # Get reschedule data
        reschedule_data = req.get_json()
        required_fields = ['date', 'startTime', 'endTime']

        for field in required_fields:
            if field not in reschedule_data:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400
                )

        # Get the session
        session = get_session(identity, session_id)
        if not session:
            return func.HttpResponse(
                json.dumps({"error": "Session not found or access denied"}),
                status_code=404
            )

        # Update session with new schedule
        updates = {
            "date": reschedule_data["date"],
            "startTime": reschedule_data["startTime"],
            "endTime": reschedule_data["endTime"],
            "rescheduled": True,
            "rescheduled_at": datetime.datetime.utcnow().isoformat()
        }

        updated_session = update_session(identity, session_id, updates)

        # Update calendar event if one exists - FIXED
        if session is not None:
            # Get the event_id safely
            event_id = None
            try:
                if isinstance(session, dict):
                    event_id = session.get("event_id")
                elif hasattr(session, "get"):
                    event_id = session.get("event_id")
                elif hasattr(session, "__getitem__"):
                    try:
                        event_id = session["event_id"]
                    except (KeyError, TypeError):
                        pass
            except Exception as e:
                print(f"Error accessing event_id: {str(e)}")

            # Only call update_calendar_event if we got an event_id
            if event_id:
                update_calendar_event(req, identity, event_id, updates)

        return func.HttpResponse(json.dumps(updated_session), status_code=200)
    except Exception as e:
        print(f"Error rescheduling session: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# === Achievements Routes ===

def get_achievements(req: func.HttpRequest) -> func.HttpResponse:
    """Get achievements for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        achievements = get_user_achievements(identity)

        # Get achievement categories for the frontend
        categories = [
            { "value": "all", "label": "All" },
            { "value": "consistency", "label": "Consistency" },
            { "value": "time", "label": "Time Management" },
            { "value": "mastery", "label": "Mastery" }
        ]

        return func.HttpResponse(
            json.dumps({
                "achievements": achievements,
                "categories": categories
            }),
            status_code=200
        )
    except Exception as e:
        print(f"Error getting achievements: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_streak(req: func.HttpRequest) -> func.HttpResponse:
    """Get study streak data for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        streak_data = get_study_streak(identity)

        # Generate recent days for streak calendar
        recent_days = generate_recent_days(streak_data)

        return func.HttpResponse(
            json.dumps({
                "streakData": streak_data,
                "recentDays": recent_days
            }),
            status_code=200
        )
    except Exception as e:
        print(f"Error getting streak data: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# === Analytics Routes ===

def get_analytics(req: func.HttpRequest) -> func.HttpResponse:
    """Get study analytics data for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get study stats
        stats = get_study_stats(identity)

        # Get module stats
        module_stats = get_module_study_stats(identity)

        # Get chart data
        module_time_distribution = get_module_time_distribution(identity)
        sessions_timeline = get_sessions_timeline(identity)
        productivity_patterns = get_productivity_patterns(identity)
        grade_distribution = get_grade_distribution_data(identity)

        return func.HttpResponse(
            json.dumps({
                "studyStats": stats,
                "moduleStudyStats": module_stats,
                "moduleTimeDistribution": module_time_distribution,
                "sessionsTimeline": sessions_timeline,
                "productivityPatterns": productivity_patterns,
                "gradeDistribution": grade_distribution
            }),
            status_code=200
        )
    except Exception as e:
        print(f"Error getting analytics data: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# === AI Tips Routes ===

def get_tips(req: func.HttpRequest) -> func.HttpResponse:
    """Get active AI tips for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        tips = get_user_ai_tips(identity)
        return func.HttpResponse(json.dumps(tips), status_code=200)
    except Exception as e:
        print(f"Error getting AI tips: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def accept_tip(req: func.HttpRequest) -> func.HttpResponse:
    """Accept and apply an AI tip"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    tip_id = req.route_params.get('id')
    if not tip_id:
        return func.HttpResponse(json.dumps({"error": "Tip ID is required"}), status_code=400)

    try:
        updated_tip = update_ai_tip_status(identity, tip_id, True, False)

        if not updated_tip:
            return func.HttpResponse(
                json.dumps({"error": "Tip not found or access denied"}),
                status_code=404
            )

        # In a real app, would apply the tip's recommendation here

        return func.HttpResponse(json.dumps(updated_tip), status_code=200)
    except Exception as e:
        print(f"Error accepting tip: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def reject_tip(req: func.HttpRequest) -> func.HttpResponse:
    """Reject an AI tip"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    tip_id = req.route_params.get('id')
    if not tip_id:
        return func.HttpResponse(json.dumps({"error": "Tip ID is required"}), status_code=400)

    try:
        updated_tip = update_ai_tip_status(identity, tip_id, False, True)

        if not updated_tip:
            return func.HttpResponse(
                json.dumps({"error": "Tip not found or access denied"}),
                status_code=404
            )

        return func.HttpResponse(json.dumps(updated_tip), status_code=200)
    except Exception as e:
        print(f"Error rejecting tip: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

# === Helper Functions ===

def get_module_by_id(user_email: str, module_id: str):
    """Get a module by ID from the user's modules"""
    modules = get_user_modules(user_email)
    for module in modules:
        if module.get("id") == module_id:
            return module
    return None

def create_sessions_from_schedule(user_email: str, schedule: dict, create_calendar_events: bool = False) -> list:
    """Create study sessions from a schedule, optionally creating calendar events"""
    sessions = []

    # Get modules
    modules = []
    for module_id in schedule["modules"]:
        module = get_module_by_id(user_email, module_id)
        if module:
            modules.append(module)

    if not modules:
        return []

    # Parse date range
    start_date = datetime.datetime.fromisoformat(schedule["start_date"].replace('Z', '+00:00')).date()
    end_date = datetime.datetime.fromisoformat(schedule["end_date"].replace('Z', '+00:00')).date()

    # Get available days
    available_days = schedule["available_days"]
    day_mapping = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }

    available_day_indices = [day_mapping[day.lower()] for day in available_days if day.lower() in day_mapping]

    # Generate sessions for each available day in the date range
    current_date = start_date
    while current_date <= end_date:
        # Check if current day is in available days
        if current_date.weekday() in available_day_indices:
            # Determine how many sessions to create for this day
            sessions_for_day = min(len(modules), schedule["max_sessions_per_day"])

            # Select modules for today (simple round-robin)
            day_modules = modules[:sessions_for_day]

            # Create sessions at preferred times
            for i, module in enumerate(day_modules):
                # Simple time assignment based on preferences
                # In a real app, would have more sophisticated scheduling
                preferred_times = schedule["preferred_times"]
                if not preferred_times:
                    preferred_times = ["morning", "afternoon", "evening"]

                # Use preference index or default to morning
                time_preference = preferred_times[i % len(preferred_times)]

                # Map preference to time
                start_time = "09:00"  # Default morning
                if time_preference == "afternoon":
                    start_time = "14:00"
                elif time_preference == "evening":
                    start_time = "18:00"
                elif time_preference == "night":
                    start_time = "20:00"

                # Calculate end time based on session duration
                start_dt = datetime.datetime.strptime(start_time, "%H:%M")
                end_dt = start_dt + datetime.timedelta(minutes=schedule["session_duration"])
                end_time = end_dt.strftime("%H:%M")

                # Create session
                session_data = {
                    "title": f"{module.get('name')} Study Session",
                    "module": module.get("id"),
                    "date": current_date.isoformat(),
                    "startTime": start_time,
                    "endTime": end_time,
                    "description": f"Study session for {module.get('name')}",
                    "status": "planned",
                    "completed": False,
                    "schedule_id": schedule["id"]
                }

                created_session = create_study_session(user_email, session_data)

                # Create calendar event for the session if requested
                if create_calendar_events:
                    event_id = create_calendar_event_for_session(None, user_email, created_session)

                    # Update session with event_id if created
                    if event_id:
                        update_session(user_email, created_session["id"], {"event_id": event_id})
                        created_session["event_id"] = event_id

                sessions.append(created_session)

        # Move to next day
        current_date += datetime.timedelta(days=1)

    return sessions

def create_calendar_event_for_session(req, user_email: str, session: dict):
    """Create a calendar event for a study session"""
    try:
        # Ensure session is a dictionary and has the required fields
        if not isinstance(session, dict):
            print(f"Session is not a dictionary: {type(session)}")
            return None

        # Prepare calendar event data
        event_data = {
            "title": session.get("title", "Study Session"),
            "description": session.get("description", f"Study session"),
            "date": session.get("date", ""),
            "start_time": session.get("startTime", ""),
            "end_time": session.get("endTime", ""),
            "all_day": False,
            "type": "study_session",  # Mark specifically as study_session type
            "color": "#9e78ff",  # Use purple for study sessions
            "user_email": user_email,
            "schedule_id": session.get("schedule_id", "")  # Include reference to the schedule
        }

        # Call create_event function
        if req:
            # If called from an HTTP request context
            try:
                # Pass the event data directly to create_event
                from calendar_routes import create_calendar_event
                event_result = create_calendar_event(user_email, event_data)
                return event_result.get("id") if event_result else None
            except Exception as e:
                print(f"Error creating event from request: {str(e)}")
                return None
        else:
            # Create event directly
            from calendar_routes import create_calendar_event
            event_result = create_calendar_event(user_email, event_data)
            return event_result.get("id") if event_result else None
    except Exception as e:
        print(f"Error creating calendar event: {str(e)}")
        return None

def update_calendar_event(req, user_email: str, event_id: str, updates: dict):
    """Update an existing calendar event"""
    try:
        # This would call your calendar update endpoint
        # Implementation depends on your calendar_routes.py
        return None
    except Exception as e:
        print(f"Error updating calendar event: {str(e)}")
        return None

def calculate_xp(session: dict, productivity: int) -> int:
    """Calculate XP earned for a completed session"""
    # Base XP for completing a session
    base_xp = 50

    # Bonus XP based on productivity rating
    productivity_bonus = productivity * 10

    # Time bonus (longer sessions earn more)
    duration_minutes = 0
    if isinstance(session, dict) and "startTime" in session and "endTime" in session:
        start = datetime.datetime.strptime(session["startTime"], "%H:%M")
        end = datetime.datetime.strptime(session["endTime"], "%H:%M")
        duration_minutes = (end - start).total_seconds() / 60

    time_bonus = int(duration_minutes / 30) * 10  # 10 XP per 30 minutes

    total_xp = base_xp + productivity_bonus + time_bonus
    return total_xp

def generate_recent_days(streak_data: dict) -> list:
    """Generate recent days data for the streak calendar"""
    recent_days = []
    today = datetime.datetime.utcnow().date()

    # Generate data for the last 14 days
    for i in range(13, -1, -1):
        day = today - datetime.timedelta(days=i)
        day_str = day.isoformat()

        # Check if studied on this day - ensure streak_data is a dict with history
        studied = False
        if isinstance(streak_data, dict) and "history" in streak_data:
            studied = streak_data["history"].get(day_str, False)

        recent_days.append({
            "date": day_str,
            "studied": studied
        })

    return recent_days

def generate_user_tips(user_email: str):
    """Generate AI tips for the user based on their study data"""
    try:
        # Get user's sessions
        sessions = get_user_sessions(user_email)

        # Get user's modules
        modules = get_user_modules(user_email)

        # Get user's study stats
        stats = get_study_stats(user_email)

        # Analyze productivity patterns
        productivity_data = get_productivity_patterns(user_email)

        # Generate tips using AI
        tips = generate_ai_tips(user_email, sessions, modules, stats, productivity_data)

        # Save tips to database
        for tip in tips:
            create_ai_tip(user_email, tip)

        return tips
    except Exception as e:
        print(f"Error generating AI tips: {str(e)}")
        return []