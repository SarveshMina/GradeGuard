# calendar_routes.py with enhanced error handling
import azure.functions as func
import json
import traceback
from models import CalendarEvent
from database import create_calendar_event, get_user_events, update_calendar_event, delete_calendar_event
from user_routes import verify_session

def get_events(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    user_email = identity
    start_date = req.params.get('start_date')
    end_date = req.params.get('end_date')

    try:
        events = get_user_events(user_email, start_date, end_date)
        return func.HttpResponse(json.dumps(events), status_code=200)
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_event(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get request body
        event_data = req.get_json()
        print(f"Received event data: {event_data}")
        
        # Explicit validation to catch issues before Pydantic
        required_fields = ['title', 'date']
        for field in required_fields:
            if field not in event_data or not event_data[field]:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400
                )
        
        try:
            # Add user_email to event data before validation
            # This fixes the validation error
            event_data['user_email'] = identity
            
            # Validate with Pydantic model
            event = CalendarEvent(**event_data)
            print(f"Validated event data: {event.dict()}")
            
            # Create event in database
            created_event = create_calendar_event(identity, event.dict(exclude_none=True))
            return func.HttpResponse(json.dumps(created_event), status_code=201)
        except Exception as e:
            print(f"Error validating event data: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": f"Validation error: {str(e)}"}),
                status_code=400
            )
    except ValueError as e:
        print(f"Invalid JSON: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON in request body"}),
            status_code=400
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(
            json.dumps({"error": f"Server error: {str(e)}"}),
            status_code=500
        )

def update_event(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    event_id = req.route_params.get('id')
    if not event_id:
        return func.HttpResponse(json.dumps({"error": "Event ID is required"}), status_code=400)

    try:
        update_data = req.get_json()
        print(f"Updating event {event_id} with data: {update_data}")
        
        try:
            # Add user_email to update data if validation requires it
            if 'user_email' not in update_data:
                update_data['user_email'] = identity
                
            updated_event = update_calendar_event(identity, event_id, update_data)
            return func.HttpResponse(json.dumps(updated_event), status_code=200)
        except Exception as e:
            print(f"Error updating event: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": f"Update error: {str(e)}"}),
                status_code=400
            )
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON in request body"}),
            status_code=400
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(
            json.dumps({"error": f"Server error: {str(e)}"}),
            status_code=500
        )

def delete_event(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    event_id = req.route_params.get('id')
    if not event_id:
        return func.HttpResponse(json.dumps({"error": "Event ID is required"}), status_code=400)

    try:
        print(f"Deleting event {event_id} for user {identity}")
        success = delete_calendar_event(identity, event_id)
        if success:
            return func.HttpResponse(json.dumps({"message": "Event deleted"}), status_code=200)
        else:
            return func.HttpResponse(json.dumps({"error": "Event not found"}), status_code=404)
    except Exception as e:
        print(f"Error deleting event: {str(e)}")
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)