# reminder_timer.py
import datetime
import logging
import azure.functions as func
from database import _container
from email_service import send_reminder_email

def main(timer: func.TimerRequest) -> None:
    """Timer trigger to process due reminders"""
    if timer.past_due:
        logging.info('The timer is past due!')

    logging.info('Reminder timer trigger function started')
    
    # Get current time
    now = datetime.datetime.utcnow()
    now_iso = now.isoformat()
    
    # Find reminders that are due but not sent yet
    query = """
    SELECT * FROM c 
    WHERE c.type = 'reminder' 
    AND c.sent = false 
    AND c.reminder_date <= @now
    """
    parameters = [{"name": "@now", "value": now_iso}]
    
    try:
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
        
        logging.info(f"Processed {len(reminders)} reminders, sent {sent_count} emails")
    except Exception as e:
        logging.error(f"Error processing reminders: {str(e)}")