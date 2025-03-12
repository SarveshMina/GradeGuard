# Create file: account_routes.py
import azure.functions as func
import json
from passlib.hash import bcrypt
from models import PasswordChange, UserSettings
from database import get_user_by_email, _container
from user_routes import verify_session

def change_password(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        body = req.get_json()
        pw_change = PasswordChange(**body)

        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Verify current password
        if not bcrypt.verify(pw_change.current_password, user_doc["password"]):
            return func.HttpResponse(json.dumps({"error": "Current password is incorrect"}), status_code=400)

        # Update to new password
        user_doc["password"] = bcrypt.hash(pw_change.new_password)
        _container.upsert_item(user_doc)

        # Send password change notification email
        try:
            from email_service import send_password_changed_email
            send_password_changed_email(identity, user_doc.get("firstName", "User"))
        except Exception as e:
            print(f"Error sending password change notification: {str(e)}")
            # Don't fail the password change if email fails

        return func.HttpResponse(json.dumps({"message": "Password updated successfully"}), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def get_settings(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Return settings or default values
        settings = user_doc.get("settings", {
            "appearance": {
                "accentColor": "purple",
                "fontSize": "medium",
                "highContrast": False
            },
            "academic": {
                "gradingScale": [
                    {"letter": "A", "minPercentage": 90, "gpaValue": 4.0},
                    {"letter": "B", "minPercentage": 80, "gpaValue": 3.0},
                    {"letter": "C", "minPercentage": 70, "gpaValue": 2.0},
                    {"letter": "D", "minPercentage": 60, "gpaValue": 1.0},
                    {"letter": "F", "minPercentage": 0, "gpaValue": 0.0}
                ],
                "termStartDate": "",
                "termEndDate": "",
                "holidays": []
            },
            "accessibility": {
                "screenReaderOptimized": False,
                "keyboardShortcuts": True,
                "focusMode": False
            },
            "calendar": {
                "firstDayOfWeek": "sunday",
                "defaultEventDuration": "60",
                "defaultEventType": "general",
                "timeFormat": "12h",
                "dateFormat": "MM/DD/YYYY"
            }
        })

        return func.HttpResponse(json.dumps(settings), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_settings(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        settings_data = req.get_json()

        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Initialize settings if not exist
        if "settings" not in user_doc:
            user_doc["settings"] = {}

        # Update with deep merge
        updated_settings = settings_data
        
        # Perform deep merge for nested objects
        deep_merge(user_doc["settings"], updated_settings)

        _container.upsert_item(user_doc)

        return func.HttpResponse(json.dumps(user_doc["settings"]), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def deep_merge(target, source):
    """Deep merge dictionaries with nested keys"""
    for key, value in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            deep_merge(target[key], value)
        else:
            target[key] = value