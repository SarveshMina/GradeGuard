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
    update_user_calculator,
    _container
)

# Session configuration
SESSION_COOKIE_NAME = "session_id"
SESSION_TIMEOUT_SECONDS = 2592000  # 30 days

def get_session(session_id: str) -> dict:
    """Get session from database instead of memory."""
    try:
        session_key = f"session:{session_id}"
        session_doc = _container.read_item(item=session_key, partition_key=session_key)
        return session_doc
    except Exception:
        return None

def create_session(email: str) -> str:
    """Create a session for the given email, store in database, return session_id."""
    session_id = uuid.uuid4().hex
    session_doc = {
        "id": f"session:{session_id}",
        "type": "session",
        "email": email,
        "created": datetime.datetime.utcnow().isoformat()
    }
    try:
        _container.create_item(body=session_doc)
    except Exception as e:
        print(f"Error creating session: {e}")
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
    
    session = get_session(session_id)
    if not session:
        return False, "Invalid session"

    # Optional: enforce actual expiration
    try:
        created = datetime.datetime.fromisoformat(session["created"])
        age_seconds = (datetime.datetime.utcnow() - created).total_seconds()
        if age_seconds > SESSION_TIMEOUT_SECONDS:
            # Session expired
            try:
                _container.delete_item(item=f"session:{session_id}", partition_key=f"session:{session_id}")
            except Exception as e:
                print(f"Error deleting expired session: {e}")
            return False, "Session expired"
    except Exception as e:
        print(f"Error checking session expiration: {e}")
        # Continue if there's an error parsing the date

    return True, session["email"]


def register_user(req: HttpRequest) -> HttpResponse:
    # (unchanged from your code)
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        user_in = User(**body)
    except ValidationError as e:
        return HttpResponse(e.json(), status_code=400, mimetype="application/json")

    if get_user_by_email(user_in.email):
        return HttpResponse(
            json.dumps({"error": "Email already in use."}),
            status_code=400,
            mimetype="application/json"
        )

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

    session_id = create_session(user_in.email)
    response = HttpResponse(
        json.dumps({"message": "User registered successfully."}),
        status_code=201,
        mimetype="application/json"
    )
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=SESSION_TIMEOUT_SECONDS)) \
                  .strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    response.headers["Set-Cookie"] = (
        f"{SESSION_COOKIE_NAME}={session_id}; "
        f"Expires={expire_time}; "
        "HttpOnly; Path=/; "
        "SameSite=None; Secure"
    )
    return response


def login_user(req: HttpRequest) -> HttpResponse:
    # (unchanged from your code)
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

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

    if not bcrypt.verify(user_in.password, user_doc["password"]):
        return HttpResponse(
            json.dumps({"error": "Invalid email or password."}),
            status_code=401,
            mimetype="application/json"
        )

    session_id = create_session(user_doc["email"])
    response = HttpResponse(
        json.dumps({"message": "Login successful."}),
        status_code=200,
        mimetype="application/json"
    )
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=SESSION_TIMEOUT_SECONDS)) \
                  .strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    response.headers["Set-Cookie"] = (
        f"{SESSION_COOKIE_NAME}={session_id}; "
        f"Expires={expire_time}; "
        "HttpOnly; Path=/; "
        "SameSite=None; Secure"
    )
    return response


def protected_resource(req: HttpRequest) -> HttpResponse:
    # (unchanged)
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
    # (unchanged)
    try:
        from database import get_all_universities_docs
        docs = get_all_universities_docs()
        return HttpResponse(json.dumps(docs), status_code=200, mimetype="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}),
                            status_code=500,
                            mimetype="application/json")


def get_university_endpoint(req: HttpRequest) -> HttpResponse:
    # (unchanged)
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
    """
    This function is called when the frontend sends a PUT request to /calculator
    with JSON like: { "numYears": 3, "semesters": 2, "credits": 90 }
    We'll build the 'years' array automatically, then store it in user_doc["calculator"].
    Or if you still want to accept an array, you can handle both.
    """
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

    # Check if the request has "numYears, semesters, credits" - i.e. from the wizard
    num_years = body.get("numYears")
    sem = body.get("semesters")
    cred = body.get("credits")

    if num_years and sem and cred:
        # We assume the user is sending the simpler object
        # Build the array
        new_years = []
        for i in range(num_years):
            new_years.append({
                "year": f"Year {i+1}",
                "active": False,
                "credits": cred,
                "weight": 0,
                # If you want to store 'semesters' for each year
                "semesters": sem
            })
        # Now store in user_doc["calculator"]["years"] = new_years
        from database import get_user_by_email, _container
        user_doc = get_user_by_email(email)
        if not user_doc:
            return HttpResponse(json.dumps({"error": "User not found."}),
                                status_code=404,
                                mimetype="application/json")

        # If user_doc doesn't have "calculator", create an empty dict
        if "calculator" not in user_doc:
            user_doc["calculator"] = {}
        user_doc["calculator"]["years"] = new_years

        # Upsert
        _container.upsert_item(user_doc)

        return HttpResponse(json.dumps({"message": "Degree configuration saved."}),
                            status_code=200,
                            mimetype="application/json")

    else:
        # Otherwise, fallback to your original logic that expects a "CalculatorConfig"
        # e.g. { "years": [ { "year": "Year 1", "active": true, "credits": 120, "weight": 0 } ... ] }
        try:
            from models import CalculatorConfig
            config = CalculatorConfig(**body)  # Will raise if invalid
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
    # (unchanged)
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
    # (unchanged)
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