# google_auth.py

import os
import json
import datetime
import uuid
import requests
from azure.functions import HttpRequest, HttpResponse

# Import helper functions from your project
from database import create_user, get_user_by_email
from user_routes import create_jwt

# Google OAuth configuration from environment variables
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

# Google endpoints
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v3/userinfo"


def google_login_redirect(req: HttpRequest) -> HttpResponse:
    """
    Redirect the user to Google OAuth 2.0 consent screen.
    """
    auth_url = (
        f"{GOOGLE_AUTH_URI}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    # Return a 302 redirect to the Google auth URL
    return HttpResponse(status_code=302, headers={"Location": auth_url})


def google_auth_callback(req: HttpRequest) -> HttpResponse:
    """
    Handle the OAuth callback from Google.
    Exchange the authorization code for tokens, fetch user info,
    create a new user record if needed, and return a JWT.
    """
    # Retrieve the code from the query parameters
    code = req.params.get("code")
    if not code:
        return HttpResponse(
            json.dumps({"error": "Missing authorization code."}),
            status_code=400,
            mimetype="application/json"
        )

    # Exchange the authorization code for tokens
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    token_response = requests.post(GOOGLE_TOKEN_URI, data=token_data)
    if token_response.status_code != 200:
        return HttpResponse(
            json.dumps({"error": "Failed to obtain tokens from Google."}),
            status_code=400,
            mimetype="application/json"
        )

    tokens = token_response.json()
    access_token = tokens.get("access_token")
    if not access_token:
        return HttpResponse(
            json.dumps({"error": "No access token returned."}),
            status_code=400,
            mimetype="application/json"
        )

    # Retrieve user information from Google using the access token
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(GOOGLE_USERINFO_URI, headers=headers)
    if userinfo_response.status_code != 200:
        return HttpResponse(
            json.dumps({"error": "Failed to fetch user info from Google."}),
            status_code=400,
            mimetype="application/json"
        )
    userinfo = userinfo_response.json()
    email = userinfo.get("email")
    first_name = userinfo.get("given_name", "User")

    # Check if the user already exists in our database
    user_doc = get_user_by_email(email)
    if not user_doc:
        # Create a new user record
        generated_userid = str(uuid.uuid4())
        user_doc = {
            "id": email,  # using email as the document ID
            "userid": generated_userid,
            "firstName": first_name,
            "email": email,
            "password": "",  # Password not needed for Google-auth users
            "university": "",  # Optional: let the user fill this in later
            "degree": "",
            "calcType": "",
            "createdAt": datetime.datetime.utcnow().isoformat()
        }
        create_user(user_doc)

    # Generate a JWT token for the user
    token = create_jwt(email)

    # Instead of returning JSON, redirect to the frontend.
    # Set your frontend URL (adjust the port/path as needed)
    frontend_redirect_url = os.environ.get("FRONTEND_REDIRECT_URL", "http://localhost:8080/dashboard")
    redirect_url = f"{frontend_redirect_url}?token={token}"
    return HttpResponse(status_code=302, headers={"Location": redirect_url})
