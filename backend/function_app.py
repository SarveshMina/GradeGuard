import azure.functions as func
from user_routes import (
    register_user,
    login_user,
    protected_resource,
    get_universities_endpoint,
    get_university_endpoint,
    search_universities_endpoint,
    update_calculator_config,
    get_calculator_config
)
import json
from google_auth import google_login_redirect, google_auth_callback
from calendar_routes import get_events, create_event, update_event, delete_event
from user_profile_routes import get_user_profile, update_user_profile, get_avatar_upload_url
from account_routes import change_password, get_settings, update_settings

# We'll also import our helper from user_routes to verify session
from user_routes import verify_session
from database import get_user_by_email, _container

ALLOWED_ORIGIN = "http://localhost:5173"

def cors_preflight_response() -> func.HttpResponse:
    headers = {
        "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
        "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Credentials": "true"
    }
    return func.HttpResponse(status_code=200, headers=headers)

def add_cors_headers(response: func.HttpResponse) -> func.HttpResponse:
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

app = func.FunctionApp()

@app.route(route="register", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def register_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = register_user(req)
    return add_cors_headers(response)

@app.route(route="login", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def login_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = login_user(req)
    return add_cors_headers(response)

@app.route(route="protected", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def protected_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = protected_resource(req)
    return add_cors_headers(response)

@app.route(route="stats/universities", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_universities(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = get_universities_endpoint(req)
    return add_cors_headers(response)

@app.route(route="stats/university", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_university(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = get_university_endpoint(req)
    return add_cors_headers(response)

@app.route(route="auth/google", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def google_login(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = google_login_redirect(req)
    return add_cors_headers(response)

@app.route(route="auth/google/callback", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def google_callback(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = google_auth_callback(req)
    return add_cors_headers(response)

@app.route(route="calculator", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def get_calculator(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = get_calculator_config(req)
    return add_cors_headers(response)

@app.route(route="calculator/update", methods=["PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def update_calculator(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = update_calculator_config(req)
    return add_cors_headers(response)

@app.route(route="universities/search", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def search_universities_route(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = search_universities_endpoint(req)
    return add_cors_headers(response)

# ---------------------------------------------------------------------------
# ENDPOINT for user config wizard: /api/user/config (GET, PUT)
# ---------------------------------------------------------------------------
@app.route(route="user/config", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def user_config_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    # Handle CORS preflight
    if req.method == "OPTIONS":
        return cors_preflight_response()

    # 1. Verify session
    is_valid, identity = verify_session(req)
    if not is_valid:
        return add_cors_headers(func.HttpResponse(
            json.dumps({"error": identity}),
            status_code=401,
            mimetype="application/json"
        ))

    # 'identity' is the user's email if valid
    user_doc = get_user_by_email(identity)
    if not user_doc:
        return add_cors_headers(func.HttpResponse(
            json.dumps({"error": "User not found."}),
            status_code=404,
            mimetype="application/json"
        ))

    # 2. GET request -> return user_doc["config"] (or empty if not set)
    if req.method == "GET":
        user_config = user_doc.get("config", {})
        return add_cors_headers(func.HttpResponse(
            json.dumps(user_config), 
            status_code=200, 
            mimetype="application/json"
        ))

    if req.method == "PUT":
        config_update = req.get_json()
        if "config" not in user_doc:
            user_doc["config"] = {}
        
        # Merge or overwrite fields
        for key, value in config_update.items():
            user_doc["config"][key] = value

        _container.upsert_item(user_doc)

        return add_cors_headers(func.HttpResponse(
            json.dumps({"message": "User config updated."}),
            status_code=200,
            mimetype="application/json"
        ))

# Combined endpoint for calendar events (GET and POST)
@app.route(route="calendar/events", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def calendar_events(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    
    if req.method == "GET":
        response = get_events(req)
    elif req.method == "POST":
        response = create_event(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )
    
    return add_cors_headers(response)


@app.route(route="calendar/events/{id}", methods=["PUT", "DELETE", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def calendar_event_by_id(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    
    if req.method == "PUT":
        response = update_event(req)
    elif req.method == "DELETE":
        response = delete_event(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )
    
    return add_cors_headers(response)

@app.route(route="user/profile", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def user_profile(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    
    if req.method == "GET":
        response = get_user_profile(req)
    elif req.method == "PUT":
        response = update_user_profile(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )
    
    return add_cors_headers(response)

@app.route(route="user/avatar-upload", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def avatar_upload(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = get_avatar_upload_url(req)
    return add_cors_headers(response)

@app.route(route="user/password", methods=["PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def password_change(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()
    response = change_password(req)
    return add_cors_headers(response)

@app.route(route="settings", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def settings_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response()

    if req.method == "GET":
        response = get_settings(req)
    elif req.method == "PUT":
        response = update_settings(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response)