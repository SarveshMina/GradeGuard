# google_auth.py

import os
import json
import datetime
import uuid
import requests
from azure.functions import HttpRequest, HttpResponse

from database import create_user, get_user_by_email
from user_routes import create_session, SESSION_COOKIE_NAME, SESSION_TIMEOUT_SECONDS

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URI = "https://www.googleapis.com/oauth2/v3/userinfo"


def google_login_redirect(req: HttpRequest) -> HttpResponse:
    auth_url = (
        f"{GOOGLE_AUTH_URI}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return HttpResponse(status_code=302, headers={"Location": auth_url})


def google_auth_callback(req: HttpRequest) -> HttpResponse:
    code = req.params.get("code")
    if not code:
        return HttpResponse(
            json.dumps({"error": "Missing authorization code."}),
            status_code=400,
            mimetype="application/json"
        )

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

    # Check existing user
    user_doc = get_user_by_email(email)
    if not user_doc:
        generated_userid = str(uuid.uuid4())
        user_doc = {
            "id": email,
            "userid": generated_userid,
            "firstName": first_name,
            "email": email,
            "password": "", 
            "university": "",
            "degree": "",
            "calcType": "",
            "createdAt": datetime.datetime.utcnow().isoformat()
        }
        create_user(user_doc)

    # Create a session
    session_id = create_session(email)
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=SESSION_TIMEOUT_SECONDS)) \
        .strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    response = HttpResponse(
        json.dumps({"message": "Authentication successful."}),
        status_code=302,
        mimetype="application/json"
    )
    # IMPORTANT: Add SameSite=None; Secure
    response.headers["Set-Cookie"] = (
        f"{SESSION_COOKIE_NAME}={session_id}; Expires={expire_time}; HttpOnly; Path=/; SameSite=None; Secure"
    )
    frontend_redirect_url = os.environ.get("FRONTEND_REDIRECT_URL", "http://localhost:8080/dashboard")
    response.headers["Location"] = frontend_redirect_url
    return response
