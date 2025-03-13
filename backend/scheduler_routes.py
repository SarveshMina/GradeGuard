# scheduler_routes.py
import azure.functions as func
import json
import traceback
import datetime
from user_routes import verify_session
from ai_scheduler import (
    get_user_study_preference,
    generate_study_schedule,
    save_study_sessions,
    create_calendar_events_from_sessions,
    update_session_status,
    get_recommendations_based_on_feedback,
    get_user_sessions
)
from ical_service import (
    import_ical_from_url,
    import_ical_from_file,
    generate_ical_export,
    create_ical_export_url,
    get_user_imported_calendars,
    import_events_to_user_module_map,
    import_ical_events
)
from database import _container, get_user_by_email
from models import StudyPreference, SessionFeedback

def get_study_preferences(req: func.HttpRequest) -> func.HttpResponse:
    """Get user's study preferences"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get study preferences
        preferences = get_user_study_preference(identity)
        
        # Return as JSON
        return func.HttpResponse(
            json.dumps(preferences.dict()),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error retrieving study preferences: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_study_preferences(req: func.HttpRequest) -> func.HttpResponse:
    """Update user's study preferences"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get request body
        preferences_data = req.get_json()
        
        # Ensure user_email is set
        preferences_data["user_email"] = identity
        
        # Validate preferences with model
        preferences = StudyPreference(**preferences_data)
        
        # Convert to dictionary and add metadata
        preferences_dict = preferences.dict()
        preferences_dict["id"] = f"study_preference_{identity}"
        preferences_dict["type"] = "study_preference"
        
        # Update in database
        _container.upsert_item(body=preferences_dict)
        
        return func.HttpResponse(
            json.dumps(preferences.dict()),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error updating study preferences: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def generate_schedule(req: func.HttpRequest) -> func.HttpResponse:
    """Generate a study schedule"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get parameters
        params = req.get_json() if req.get_body() else {}
        start_date = params.get("start_date")  # ISO format date
        days_ahead = params.get("days_ahead", 14)  # Default to 2 weeks ahead
        save_to_calendar = params.get("save_to_calendar", False)  # Whether to save to calendar directly
        
        # Generate schedule
        study_sessions = generate_study_schedule(identity, start_date, days_ahead)
        
        if not study_sessions:
            return func.HttpResponse(
                json.dumps({
                    "error": "Failed to generate study schedule", 
                    "message": "Try updating your study preferences or adding more modules"
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Save sessions and create calendar events if requested
        if save_to_calendar:
            saved_sessions = save_study_sessions(study_sessions)
            calendar_events = create_calendar_events_from_sessions(study_sessions)
            
            return func.HttpResponse(
                json.dumps({
                    "message": "Study schedule generated and saved to calendar",
                    "sessions": [s.dict() for s in study_sessions],
                    "calendar_events": calendar_events
                }),
                status_code=200,
                mimetype="application/json"
            )
        
        # Otherwise just return the generated schedule
        return func.HttpResponse(
            json.dumps({
                "message": "Study schedule generated",
                "sessions": [s.dict() for s in study_sessions]
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error generating study schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def save_schedule(req: func.HttpRequest) -> func.HttpResponse:
    """Save a generated study schedule"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get sessions from request
        sessions_data = req.get_json()
        
        # Validate and convert to model instances
        study_sessions = []
        for session_data in sessions_data:
            # Ensure user_email is set correctly
            session_data["user_email"] = identity
            study_sessions.append(StudyPreference(**session_data))
        
        # Save sessions
        saved_sessions = save_study_sessions(study_sessions)
        
        # Create calendar events
        calendar_events = create_calendar_events_from_sessions(study_sessions)
        
        return func.HttpResponse(
            json.dumps({
                "message": "Study schedule saved",
                "sessions": saved_sessions,
                "calendar_events": calendar_events
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error saving study schedule: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def get_study_sessions(req: func.HttpRequest) -> func.HttpResponse:
    """Get user's study sessions"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get filter parameters
        status = req.params.get("status")  # scheduled, completed, missed, rescheduled
        start_date = req.params.get("start_date")
        end_date = req.params.get("end_date")
        
        # Get sessions
        sessions = get_user_sessions(identity, status, start_date, end_date)
        
        return func.HttpResponse(
            json.dumps([s.dict() for s in sessions]),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error getting study sessions: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_session(req: func.HttpRequest) -> func.HttpResponse:
    """Update a study session status and feedback"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    session_id = req.route_params.get('id')
    if not session_id:
        return func.HttpResponse(json.dumps({"error": "Session ID is required"}), status_code=400)

    try:
        # Get request body
        update_data = req.get_json()
        
        # Get status and feedback
        status = update_data.get("status")
        feedback = update_data.get("feedback")
        
        if not status:
            return func.HttpResponse(json.dumps({"error": "Status is required"}), status_code=400)
        
        # Validate feedback if provided
        if feedback:
            # Add session_id to feedback
            feedback["session_id"] = session_id
            feedback = SessionFeedback(**feedback).dict()
        
        # Update session
        updated_session = update_session_status(session_id, status, feedback)
        
        if not updated_session:
            return func.HttpResponse(
                json.dumps({"error": "Session not found or update failed"}),
                status_code=404,
                mimetype="application/json"
            )
        
        return func.HttpResponse(
            json.dumps(updated_session),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error updating study session: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def get_recommendations(req: func.HttpRequest) -> func.HttpResponse:
    """Get study recommendations based on feedback"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Generate recommendations
        recommendations = get_recommendations_based_on_feedback(identity)
        
        return func.HttpResponse(
            json.dumps(recommendations),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def import_calendar(req: func.HttpRequest) -> func.HttpResponse:
    """Import a calendar from iCal URL"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get request body
        import_data = req.get_json()
        
        calendar_name = import_data.get("name")
        url = import_data.get("url")
        
        if not calendar_name or not url:
            return func.HttpResponse(
                json.dumps({"error": "Calendar name and URL are required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Import calendar
        result = import_ical_from_url(identity, calendar_name, url)
        
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error importing calendar: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def upload_calendar_file(req: func.HttpRequest) -> func.HttpResponse:
    """Import a calendar from an uploaded iCal file"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get file content
        file_content = req.get_body().decode('utf-8')
        
        # Get calendar name from form data or params
        calendar_name = req.params.get("name", "Uploaded Calendar")
        
        # Import calendar
        result = import_ical_from_file(identity, calendar_name, file_content)
        
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error uploading calendar file: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def get_imported_calendars(req: func.HttpRequest) -> func.HttpResponse:
    """Get user's imported calendars"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get calendars
        calendars = get_user_imported_calendars(identity)
        
        return func.HttpResponse(
            json.dumps([c.dict() for c in calendars]),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error getting imported calendars: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def export_calendar(req: func.HttpRequest) -> func.HttpResponse:
    """Export user's calendar as iCal"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get parameters
        include_study_sessions = req.params.get("include_study_sessions", "true").lower() == "true"
        generate_url = req.params.get("generate_url", "false").lower() == "true"
        
        if generate_url:
            # Generate a shareable URL
            url = create_ical_export_url(identity)
            
            return func.HttpResponse(
                json.dumps({"url": url}),
                status_code=200,
                mimetype="application/json"
            )
        else:
            # Generate iCal content directly
            ical_content = generate_ical_export(identity, include_study_sessions)
            
            # Return as file download
            return func.HttpResponse(
                ical_content,
                status_code=200,
                mimetype="text/calendar",
                headers={
                    "Content-Disposition": "attachment; filename=calendar.ics"
                }
            )
    except Exception as e:
        print(f"Error exporting calendar: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_module_mapping(req: func.HttpRequest) -> func.HttpResponse:
    """Get mapping of timetable events to user modules"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Generate module mapping
        mapping = import_events_to_user_module_map(identity)
        
        return func.HttpResponse(
            json.dumps(mapping),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error getting module mapping: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_module_mapping(req: func.HttpRequest) -> func.HttpResponse:
    """Update mapping of timetable events to user modules"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get mapping data
        mapping_data = req.get_json()
        
        # Update all affected events
        for module_pattern, module_ids in mapping_data.items():
            # Skip if no module IDs assigned
            if not module_ids:
                continue
            
            # Get first module ID (only use one mapping per pattern)
            module_id = module_ids[0]
            
            # Get events with this pattern
            query = f"""
            SELECT * FROM c 
            WHERE c.user_email = '{identity}' 
            AND IS_DEFINED(c.detected_module)
            AND c.detected_module = '{module_pattern}'
            """
            
            events = list(_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            # Update each event
            for event in events:
                event["module_id"] = module_id
                
                # Look up module name
                module_query = f"SELECT c.name FROM c WHERE c.id = '{module_id}'"
                modules = list(_container.query_items(
                    query=module_query,
                    enable_cross_partition_query=True
                ))
                
                if modules:
                    event["module_name"] = modules[0]["name"]
                
                # Update in database
                _container.upsert_item(body=event)
        
        return func.HttpResponse(
            json.dumps({"message": "Module mapping updated"}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error updating module mapping: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def sync_imported_calendar(req: func.HttpRequest) -> func.HttpResponse:
    """Sync a specific imported calendar"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    calendar_id = req.route_params.get('id')
    if not calendar_id:
        return func.HttpResponse(json.dumps({"error": "Calendar ID is required"}), status_code=400)

    try:
        # Get the calendar
        query = f"SELECT * FROM c WHERE c.id = '{calendar_id}' AND c.user_email = '{identity}'"
        
        calendars = list(_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if not calendars:
            return func.HttpResponse(
                json.dumps({"error": "Calendar not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        calendar = calendars[0]
        
        # Check if URL is available
        if not calendar.get("url"):
            return func.HttpResponse(
                json.dumps({"error": "Calendar has no URL to sync"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Import events from the calendar
        events, modules = import_ical_events(identity, calendar["url"])
        
        # Update last sync time
        calendar["last_sync"] = datetime.datetime.utcnow().isoformat()
        _container.upsert_item(body=calendar)
        
        return func.HttpResponse(
            json.dumps({
                "message": "Calendar synced successfully",
                "events_imported": len(events),
                "modules_detected": len(modules)
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(f"Error syncing calendar: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)