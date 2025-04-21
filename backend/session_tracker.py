# session_tracker.py
import datetime
import logging
import azure.functions as func
from study_database import update_session_statuses_automatically, get_sessions_requiring_status_update
from database import _container

def main(timer: func.TimerRequest) -> None:
    """Timer trigger to update session statuses automatically"""
    if timer.past_due:
        logging.info('Session tracker timer is past due!')

    logging.info('Session tracker timer function started')

    try:
        # Update session statuses based on current time
        updated_count = update_session_statuses_automatically()
        logging.info(f"Updated {updated_count} session statuses")
        
        # Log upcoming sessions that need attention
        upcoming_sessions = get_sessions_requiring_status_update()
        logging.info(f"Found {len(upcoming_sessions)} sessions requiring status updates")
        
        # Send optional reminders for sessions starting soon
        # (This would be implemented in a separate function)
        
    except Exception as e:
        logging.error(f"Error in session tracker: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())