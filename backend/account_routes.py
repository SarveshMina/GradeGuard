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
            "dark_mode": False,
            "notifications_enabled": True,
            "calendar_view": "month",
            "language": "en"
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
        settings = UserSettings(**settings_data)
        
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
        
        # Initialize settings if not exist
        if "settings" not in user_doc:
            user_doc["settings"] = {}
        
        # Update with new values
        updated_settings = settings.dict(exclude_none=True)
        for key, value in updated_settings.items():
            user_doc["settings"][key] = value
        
        _container.upsert_item(user_doc)
        
        return func.HttpResponse(json.dumps(user_doc["settings"]), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)