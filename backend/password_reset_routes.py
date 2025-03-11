# password_reset_routes.py
import azure.functions as func
import json
from passlib.hash import bcrypt
from database import get_user_by_email, _container
from email_service import send_password_reset_email, verify_reset_token, invalidate_reset_token

def request_password_reset(req: func.HttpRequest) -> func.HttpResponse:
    """Handle password reset request and send email with reset link"""
    try:
        # Get email from request body
        body = req.get_json()
        email = body.get("email")
        
        if not email:
            return func.HttpResponse(
                json.dumps({"error": "Email is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Check if user exists (don't reveal if user exists or not in response)
        user_exists = get_user_by_email(email) is not None
        
        # Send reset email if user exists
        if user_exists:
            send_password_reset_email(email)
        
        # Always return success to prevent email enumeration
        return func.HttpResponse(
            json.dumps({"message": "If your email is registered, you will receive a password reset link"}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": "An error occurred processing your request"}),
            status_code=500,
            mimetype="application/json"
        )

def reset_password(req: func.HttpRequest) -> func.HttpResponse:
    """Reset password using reset token"""
    try:
        # Get token and new password from request body
        body = req.get_json()
        token = body.get("token")
        new_password = body.get("password")
        
        if not token or not new_password:
            return func.HttpResponse(
                json.dumps({"error": "Token and password are required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Verify token and get user email
        user_email = verify_reset_token(token)
        if not user_email:
            return func.HttpResponse(
                json.dumps({"error": "Invalid or expired token"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get user document
        user_doc = get_user_by_email(user_email)
        if not user_doc:
            return func.HttpResponse(
                json.dumps({"error": "User not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        # Update password
        user_doc["password"] = bcrypt.hash(new_password)
        _container.upsert_item(user_doc)
        
        # Invalidate token
        invalidate_reset_token(token)
        
        # Send password change notification
        from email_service import send_password_changed_email
        send_password_changed_email(user_email, user_doc.get("firstName", "User"))
        
        return func.HttpResponse(
            json.dumps({"message": "Password reset successful"}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": "An error occurred processing your request"}),
            status_code=500,
            mimetype="application/json"
        )

def verify_token(req: func.HttpRequest) -> func.HttpResponse:
    """Verify if a reset token is valid"""
    try:
        # Get token from query parameter
        token = req.params.get("token")
        
        if not token:
            return func.HttpResponse(
                json.dumps({"error": "Token is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Verify token
        user_email = verify_reset_token(token)
        if not user_email:
            return func.HttpResponse(
                json.dumps({"valid": False}),
                status_code=200,
                mimetype="application/json"
            )
        
        return func.HttpResponse(
            json.dumps({"valid": True, "email": user_email}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": "An error occurred processing your request"}),
            status_code=500,
            mimetype="application/json"
        )