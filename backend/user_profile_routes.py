# Create file: user_profile_routes.py
import azure.functions as func
import json
from models import UserProfileUpdate
from database import get_user_by_email, _container
from user_routes import verify_session

def get_user_profile(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    user_email = identity
    try:
        user_doc = get_user_by_email(user_email)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
        
        # Return only profile fields
        profile = {
            "firstName": user_doc.get("firstName", ""),
            "lastName": user_doc.get("lastName", ""),
            "email": user_doc.get("email", ""),
            "avatar": user_doc.get("avatar", ""),
            "dateOfBirth": user_doc.get("dateOfBirth", ""),
            "phone": user_doc.get("phone", ""),
            "bio": user_doc.get("bio", ""),
            "university": user_doc.get("university", ""),
            "degree": user_doc.get("degree", "")
        }
        
        return func.HttpResponse(json.dumps(profile), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_user_profile(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    user_email = identity
    try:
        profile_data = req.get_json()
        user_doc = get_user_by_email(user_email)
        
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
        
        # Validate with model
        profile_update = UserProfileUpdate(**profile_data)
        update_dict = profile_update.dict(exclude_none=True)
        
        # Update fields
        for key, value in update_dict.items():
            user_doc[key] = value
        
        # Save updates
        _container.upsert_item(user_doc)
        
        # Return updated profile
        updated_profile = {
            "firstName": user_doc.get("firstName", ""),
            "lastName": user_doc.get("lastName", ""),
            "email": user_doc.get("email", ""),
            "avatar": user_doc.get("avatar", ""),
            "dateOfBirth": user_doc.get("dateOfBirth", ""),
            "phone": user_doc.get("phone", ""),
            "bio": user_doc.get("bio", "")
        }
        
        return func.HttpResponse(json.dumps(updated_profile), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)
    

from blob_storage import generate_avatar_upload_url

def get_avatar_upload_url(req: func.HttpRequest) -> func.HttpResponse:
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        body = req.get_json()
        filename = body.get("filename")
        
        if not filename:
            return func.HttpResponse(json.dumps({"error": "Filename is required"}), status_code=400)
        
        upload_url, public_url = generate_avatar_upload_url(identity, filename)
        
        return func.HttpResponse(
            json.dumps({
                "uploadUrl": upload_url,
                "avatarUrl": public_url
            }), 
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)