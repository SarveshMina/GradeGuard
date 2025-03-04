# Create new file: calendar_routes.py
import azure.functions as func
import json
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
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_event(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        event_data = req.get_json()
        event = CalendarEvent(**event_data)
        created_event = create_calendar_event(identity, event.dict(exclude_none=True))
        return func.HttpResponse(json.dumps(created_event), status_code=201)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def update_event(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    event_id = req.route_params.get('id')
    if not event_id:
        return func.HttpResponse(json.dumps({"error": "Event ID is required"}), status_code=400)
    
    try:
        update_data = req.get_json()
        updated_event = update_calendar_event(identity, event_id, update_data)
        return func.HttpResponse(json.dumps(updated_event), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def delete_event(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    event_id = req.route_params.get('id')
    if not event_id:
        return func.HttpResponse(json.dumps({"error": "Event ID is required"}), status_code=400)
    
    try:
        success = delete_calendar_event(identity, event_id)
        if success:
            return func.HttpResponse(json.dumps({"message": "Event deleted"}), status_code=200)
        else:
            return func.HttpResponse(json.dumps({"error": "Event not found"}), status_code=404)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)