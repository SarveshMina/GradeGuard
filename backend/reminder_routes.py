# -*- coding: utf-8 -*-
# reminder_routes.py
import azure.functions as func
import json
from datetime import datetime, timedelta
from database import _container
from user_routes import verify_session
from email_service import send_reminder_email

def create_reminder(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new reminder for an event"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get reminder data from request
        reminder_data = req.get_json()
        # Validate required fields
        required_fields = ['event_id', 'event_title', 'reminder_date', 'event_date']
        for field in required_fields:
            if field not in reminder_data:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400
                )
        
        # Add reminder metadata
        reminder_id = reminder_data.get('id') or f"reminder_{datetime.utcnow().timestamp()}"
        reminder_data['id'] = reminder_id
        reminder_data['user_email'] = identity
        reminder_data['type'] = 'reminder'
        reminder_data['created_at'] = datetime.utcnow().isoformat()
        reminder_data['sent'] = False
        
        # Save to database
        _container.upsert_item(reminder_data)
        
        return func.HttpResponse(
            json.dumps({"message": "Reminder created successfully", "id": reminder_id}),
            status_code=201
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_reminders(req: func.HttpRequest) -> func.HttpResponse:
    """Get all reminders for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Query reminders for the user
        query = "SELECT * FROM c WHERE c.type = 'reminder' AND c.user_email = @email"
        parameters = [{"name": "@email", "value": identity}]
        
        reminders = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return func.HttpResponse(json.dumps(reminders), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def delete_reminder(req: func.HttpRequest) -> func.HttpResponse:
    """Delete a reminder"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    reminder_id = req.route_params.get('id')
    if not reminder_id:
        return func.HttpResponse(json.dumps({"error": "Reminder ID is required"}), status_code=400)
    
    try:
        # First verify the reminder belongs to the user
        query = "SELECT * FROM c WHERE c.id = @id AND c.user_email = @email AND c.type = 'reminder'"
        parameters = [
            {"name": "@id", "value": reminder_id},
            {"name": "@email", "value": identity}
        ]
        
        reminders = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if not reminders:
            return func.HttpResponse(json.dumps({"error": "Reminder not found or access denied"}), status_code=404)
        
        # Delete the reminder
        _container.delete_item(item=reminder_id, partition_key=reminder_id)
        
        return func.HttpResponse(json.dumps({"message": "Reminder deleted successfully"}), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def process_reminders(req: func.HttpRequest) -> func.HttpResponse:
    """Process due reminders and send notification emails (to be called by a timer trigger)"""
    try:
        # Get current time
        now = datetime.utcnow()
        now_iso = now.isoformat()
        
        # Find reminders that are due but not sent yet
        query = """
        SELECT * FROM c 
        WHERE c.type = 'reminder' 
        AND c.sent = false 
        AND c.reminder_date <= @now
        """
        parameters = [{"name": "@now", "value": now_iso}]
        
        reminders = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        sent_count = 0
        
        # Process each reminder
        for reminder in reminders:
            user_email = reminder.get('user_email')
            event_title = reminder.get('event_title')
            event_date = reminder.get('event_date')
            event_time = reminder.get('event_time')
            
            # Send reminder email
            success = send_reminder_email(user_email, event_title, event_date, event_time)
            
            if success:
                # Mark reminder as sent
                reminder['sent'] = True
                reminder['sent_at'] = now_iso
                _container.upsert_item(reminder)
                sent_count += 1
        
        return func.HttpResponse(
            json.dumps({"message": f"Processed {len(reminders)} reminders, sent {sent_count} emails"}),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_event_reminder(req: func.HttpRequest) -> func.HttpResponse:
    """Create a reminder for a calendar event"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        data = req.get_json()
        event_id = data.get('event_id')
        days_before = int(data.get('days_before', 1))
        
        if not event_id:
            return func.HttpResponse(json.dumps({"error": "Event ID is required"}), status_code=400)
        
        # Query the event
        query = "SELECT * FROM c WHERE c.id = @id AND c.user_email = @email"
        parameters = [
            {"name": "@id", "value": event_id},
            {"name": "@email", "value": identity}
        ]
        
        events = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if not events:
            return func.HttpResponse(json.dumps({"error": "Event not found"}), status_code=404)
        
        event = events[0]
        
        # Calculate reminder date (X days before event)
        event_date = datetime.fromisoformat(event.get('date').replace('Z', '+00:00'))
        reminder_date = event_date - timedelta(days=days_before)
        
        # Create reminder
        reminder_data = {
            'id': f"reminder_{event_id}_{days_before}",
            'user_email': identity,
            'type': 'reminder',
            'event_id': event_id,
            'event_title': event.get('title'),
            'event_date': event.get('date'),
            'event_time': event.get('start_time') if not event.get('all_day', True) else None,
            'reminder_date': reminder_date.isoformat(),
            'days_before': days_before,
            'created_at': datetime.utcnow().isoformat(),
            'sent': False
        }
        
        # Save to database
        _container.upsert_item(reminder_data)
        
        return func.HttpResponse(
            json.dumps({"message": "Event reminder created successfully", "id": reminder_data['id']}),
            status_code=201
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)