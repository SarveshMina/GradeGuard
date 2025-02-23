# user_routes.py

import os
import json
import datetime
import uuid
from passlib.hash import bcrypt
from pydantic import ValidationError
from azure.functions import HttpRequest, HttpResponse

from models import User, UserLogin
from database import (
    create_user,
    get_user_by_email,
    increment_university_and_major_counter,
    get_university_doc,
    search_universities,
    update_user_calculator
)

# In-memory session store (NOT for production)
SESSIONS = {}  # session_id -> {"email": ..., "created": datetime}
SESSION_COOKIE_NAME = "session_id"
SESSION_TIMEOUT_SECONDS = 2592000  # 30 days

def create_session(email: str) -> str:
    """Create a session for the given email, store in SESSIONS dict, return session_id."""
    session_id = uuid.uuid4().hex
    SESSIONS[session_id] = {
        "email": email,
        "created": datetime.datetime.utcnow()
    }
    return session_id

def parse_cookies(req: HttpRequest) -> dict:
    cookies = {}
    cookie_header = req.headers.get("Cookie")
    if cookie_header:
        parts = cookie_header.split(";")
        for part in parts:
            if "=" in part:
                name, value = part.strip().split("=", 1)
                cookies[name] = value
    return cookies

def verify_session(req: HttpRequest) -> (bool, str):
    """Check session_id cookie, return (True, email) if valid, else (False, error)."""
    cookies = parse_cookies(req)
    session_id = cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        return False, "Missing session_id cookie"
    session = SESSIONS.get(session_id)
    if not session:
        return False, "Invalid session"

    # Optional: enforce actual expiration
    created = session["created"]
    age_seconds = (datetime.datetime.utcnow() - created).total_seconds()
    if age_seconds > SESSION_TIMEOUT_SECONDS:
        # Session expired
        del SESSIONS[session_id]
        return False, "Session expired"

    return True, session["email"]

def register_user(req: HttpRequest) -> HttpResponse:
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

    # Validate the incoming user data
    try:
        user_in = User(**body)
    except ValidationError as e:
        return HttpResponse(e.json(), status_code=400, mimetype="application/json")

    # Check if user already exists
    if get_user_by_email(user_in.email):
        return HttpResponse(
            json.dumps({"error": "Email already in use."}),
            status_code=400,
            mimetype="application/json"
        )

    # Create user doc
    generated_userid = str(uuid.uuid4())
    hashed_password = bcrypt.hash(user_in.password)
    user_doc = {
        "id": user_in.email,  # email as partition key
        "userid": generated_userid,
        "firstName": user_in.firstName,
        "email": user_in.email,
        "password": hashed_password,
        "university": user_in.university,
        "degree": user_in.degree,
        "calcType": user_in.calcType,
        "createdAt": datetime.datetime.utcnow().isoformat()
    }
    create_user(user_doc)
    increment_university_and_major_counter(user_in.university, user_in.degree)

    # Automatically log in the user (session-based)
    session_id = create_session(user_in.email)
    response = HttpResponse(
        json.dumps({"message": "User registered successfully."}),
        status_code=201,
        mimetype="application/json"
    )

    # 30-day expiration
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=SESSION_TIMEOUT_SECONDS)) \
                  .strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    # IMPORTANT: Add SameSite=None; Secure for cross-site
    response.headers["Set-Cookie"] = (
        f"{SESSION_COOKIE_NAME}={session_id}; "
        f"Expires={expire_time}; "
        "HttpOnly; Path=/; "
        "SameSite=None; Secure"
    )
    return response

def login_user(req: HttpRequest) -> HttpResponse:
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

    # Validate login data
    try:
        user_in = UserLogin(**body)
    except ValidationError as e:
        return HttpResponse(e.json(), status_code=400, mimetype="application/json")

    user_doc = get_user_by_email(user_in.email)
    if not user_doc:
        return HttpResponse(
            json.dumps({"error": "Invalid email or password."}),
            status_code=401,
            mimetype="application/json"
        )

    # Verify password
    if not bcrypt.verify(user_in.password, user_doc["password"]):
        return HttpResponse(
            json.dumps({"error": "Invalid email or password."}),
            status_code=401,
            mimetype="application/json"
        )

    # Create session
    session_id = create_session(user_doc["email"])
    response = HttpResponse(
        json.dumps({"message": "Login successful."}),
        status_code=200,
        mimetype="application/json"
    )
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=SESSION_TIMEOUT_SECONDS)) \
                  .strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    # IMPORTANT: Add SameSite=None; Secure for cross-site
    response.headers["Set-Cookie"] = (
        f"{SESSION_COOKIE_NAME}={session_id}; "
        f"Expires={expire_time}; "
        "HttpOnly; Path=/; "
        "SameSite=None; Secure"
    )
    return response

def protected_resource(req: HttpRequest) -> HttpResponse:
    is_valid, result = verify_session(req)
    if not is_valid:
        return HttpResponse(
            json.dumps({"error": result}),
            status_code=401,
            mimetype="application/json"
        )
    email = result
    return HttpResponse(
        json.dumps({"message": f"You are authorized! Session belongs to {email}."}),
        status_code=200,
        mimetype="application/json"
    )

def get_universities_endpoint(req: HttpRequest) -> HttpResponse:
    try:
        from database import get_all_universities_docs
        docs = get_all_universities_docs()
        return HttpResponse(json.dumps(docs), status_code=200, mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}),
                            status_code=500,
                            mimetype="application/json")

def get_university_endpoint(req: HttpRequest) -> HttpResponse:
    name = req.params.get("name")
    if not name:
        return HttpResponse(
            json.dumps({"error": "Missing 'name' query parameter"}),
            status_code=400,
            mimetype="application/json"
        )
    try:
        doc = get_university_doc(name)
        if not doc:
            return HttpResponse(
                json.dumps({"error": "University not found."}),
                status_code=404,
                mimetype="application/json"
            )
        return HttpResponse(json.dumps(doc), status_code=200, mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}),
                            status_code=500,
                            mimetype="application/json")

def update_calculator_config(req: HttpRequest) -> HttpResponse:
    is_valid, result = verify_session(req)
    if not is_valid:
        return HttpResponse(json.dumps({"error": result}),
                            status_code=401,
                            mimetype="application/json")
    email = result
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(json.dumps({"error": "Invalid JSON in request body."}),
                            status_code=400,
                            mimetype="application/json")
    try:
        from models import CalculatorConfig
        config = CalculatorConfig(**body)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}),
                            status_code=400,
                            mimetype="application/json")
    try:
        update_user_calculator(email, config.dict())
        return HttpResponse(json.dumps({"message": "Calculator configuration updated successfully."}),
                            status_code=200,
                            mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}),
                            status_code=500,
                            mimetype="application/json")

def get_calculator_config(req: HttpRequest) -> HttpResponse:
    is_valid, result = verify_session(req)
    if not is_valid:
        return HttpResponse(json.dumps({"error": result}),
                            status_code=401,
                            mimetype="application/json")
    email = result
    user_doc = get_user_by_email(email)
    if not user_doc:
        return HttpResponse(json.dumps({"error": "User not found."}),
                            status_code=404,
                            mimetype="application/json")
    config = user_doc.get("calculator", {})
    return HttpResponse(json.dumps(config), status_code=200, mimetype="application/json")

def search_universities_endpoint(req: HttpRequest) -> HttpResponse:
    query = req.params.get("query")
    if not query:
        return HttpResponse(json.dumps({"error": "Missing 'query' parameter"}),
                            status_code=400,
                            mimetype="application/json")
    try:
        limit = int(req.params.get("limit", 10))
        offset = int(req.params.get("offset", 0))
    except Exception:
        return HttpResponse(json.dumps({"error": "Invalid pagination parameters."}),
                            status_code=400,
                            mimetype="application/json")
    try:
        results = search_universities(query, limit=limit, offset=offset)
        return HttpResponse(json.dumps(results), status_code=200, mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}),
                            status_code=500,
                            mimetype="application/json")
