import azure.functions as func
import json
import sys
import os
import logging

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


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
from google_auth import google_login_redirect, google_auth_callback
from calendar_routes import get_events, create_event, update_event, delete_event
from user_profile_routes import get_user_profile, update_user_profile, get_avatar_upload_url
from account_routes import change_password, get_settings, update_settings
from module_routes import (
    get_all_modules,
    get_module,
    create_module,
    update_module,
    delete_module,
    get_modules_by_year_semester,
    get_module_suggestions
)
from dashboard_routes import (
    get_dashboard_data,
    update_dashboard_config,
    add_activity,
    update_goals,
    get_insights
)
from university_routes import (
    get_university_modules,
    get_degree_requirements,
    import_template_modules
)

from study_routes import (
    get_schedules, create_schedule_manual, create_schedule_ai, update_schedule_route, delete_schedule_route,
    get_active_schedule_route, activate_schedule_route, create_calendar_events_route,
    get_sessions, start_session, complete_session, reschedule_session,
    get_achievements, get_streak,
    get_analytics,
    get_tips, accept_tip, reject_tip,
    get_completion_analytics_route, get_completion_insights_route,
    rate_ai_schedule, analyze_schedule_modifications, get_schedule_explanations
)

from user_routes import verify_session, logout_user
from database import get_user_by_email, _container
from onboarding_routes import get_onboarding_status, save_onboarding_questionnaire
from module_routes import get_module_analytics
from password_reset_routes import request_password_reset, reset_password, verify_token
from reminder_routes import create_reminder, get_reminders, delete_reminder, process_reminders, create_event_reminder


# Configure CORS settings - UPDATED FOR MULTIPLE ENVIRONMENTS
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173,https://sarveshmina.co.uk").split(",")
DEFAULT_ORIGIN = ALLOWED_ORIGINS[0]

def is_allowed_origin(origin):
    # Check if the origin is in our allowed list, or allow all if "*" is in the list
    return "*" in ALLOWED_ORIGINS or origin in ALLOWED_ORIGINS

def cors_preflight_response(req: func.HttpRequest = None) -> func.HttpResponse:
    # Get the Origin header from the request if available
    requested_origin = req.headers.get("Origin", DEFAULT_ORIGIN) if req else DEFAULT_ORIGIN
    origin = requested_origin if is_allowed_origin(requested_origin) else DEFAULT_ORIGIN

    headers = {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "86400"  # 24 hours cache for preflight requests
    }
    return func.HttpResponse(status_code=200, headers=headers)

def add_cors_headers(response: func.HttpResponse, req: func.HttpRequest = None) -> func.HttpResponse:
    # Get the Origin header from the request if available
    requested_origin = req.headers.get("Origin", DEFAULT_ORIGIN) if req else DEFAULT_ORIGIN
    origin = requested_origin if is_allowed_origin(requested_origin) else DEFAULT_ORIGIN

    # Set CORS headers on the response
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    
    # Log detailed CORS information for debugging
    logging.info(f"Setting CORS headers for origin: {origin}")
    logging.info(f"Request origin: {requested_origin}")
    logging.info(f"Response headers: {dict(response.headers)}")
    
    return response

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="register", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def register_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = register_user(req)
    return add_cors_headers(response, req)

@app.route(route="login", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def login_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = login_user(req)
    return add_cors_headers(response, req)

@app.route(route="protected", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def protected_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = protected_resource(req)
    return add_cors_headers(response, req)

@app.route(route="stats/universities", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_universities(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_universities_endpoint(req)
    return add_cors_headers(response, req)

@app.route(route="stats/university", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_university(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_university_endpoint(req)
    return add_cors_headers(response, req)

@app.route(route="auth/google", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def google_login(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = google_login_redirect(req)
    return add_cors_headers(response, req)

@app.route(route="auth/google/callback", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def google_callback(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = google_auth_callback(req)
    return add_cors_headers(response, req)

@app.route(route="calculator", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def get_calculator(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_calculator_config(req)
    return add_cors_headers(response, req)

@app.route(route="calculator/update", methods=["PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def update_calculator(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = update_calculator_config(req)
    return add_cors_headers(response, req)

@app.route(route="universities/search", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def search_universities_route(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = search_universities_endpoint(req)
    return add_cors_headers(response, req)

@app.route(route="user/config", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def user_config_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    # Handle CORS preflight
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    # 1. Verify session
    is_valid, identity = verify_session(req)
    if not is_valid:
        response = func.HttpResponse(
            json.dumps({"error": identity}),
            status_code=401,
            mimetype="application/json"
        )
        return add_cors_headers(response, req)

    # 'identity' is the user's email if valid
    user_doc = get_user_by_email(identity)
    if not user_doc:
        response = func.HttpResponse(
            json.dumps({"error": "User not found."}),
            status_code=404,
            mimetype="application/json"
        )
        return add_cors_headers(response, req)

    # 2. GET request -> return user_doc["config"] (or empty if not set)
    if req.method == "GET":
        user_config = user_doc.get("config", {})
        response = func.HttpResponse(
            json.dumps(user_config),
            status_code=200,
            mimetype="application/json"
        )
        return add_cors_headers(response, req)

    if req.method == "PUT":
        config_update = req.get_json()
        if "config" not in user_doc:
            user_doc["config"] = {}

        # Merge or overwrite fields
        for key, value in config_update.items():
            user_doc["config"][key] = value

        _container.upsert_item(user_doc)

        response = func.HttpResponse(
            json.dumps({"message": "User config updated."}),
            status_code=200,
            mimetype="application/json"
        )
        return add_cors_headers(response, req)

@app.route(route="calendar/events", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def calendar_events(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

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

    return add_cors_headers(response, req)

@app.route(route="calendar/events/{id}", methods=["PUT", "DELETE", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def calendar_event_by_id(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

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

    return add_cors_headers(response, req)

@app.route(route="user/profile", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def user_profile(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

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

    return add_cors_headers(response, req)

@app.route(route="user/avatar-upload", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def avatar_upload(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_avatar_upload_url(req)
    return add_cors_headers(response, req)

@app.route(route="user/password", methods=["PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def password_change(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = change_password(req)
    return add_cors_headers(response, req)

@app.route(route="user/settings", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def settings_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

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

    return add_cors_headers(response, req)

@app.route(route="modules", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def modules_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    if req.method == "GET":
        response = get_all_modules(req)
    elif req.method == "POST":
        response = create_module(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response, req)

@app.route(route="modules/{id}", methods=["GET", "PUT", "DELETE", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def module_by_id_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    if req.method == "GET":
        response = get_module(req)
    elif req.method == "PUT":
        response = update_module(req)
    elif req.method == "DELETE":
        response = delete_module(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response, req)

@app.route(route="dashboard", methods=["GET", "PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def dashboard_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    if req.method == "GET":
        response = get_dashboard_data(req)
    elif req.method == "PUT":
        response = update_dashboard_config(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response, req)

@app.route(route="dashboard/activity", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def activity_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    if req.method == "POST":
        response = add_activity(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response, req)

@app.route(route="dashboard/goals", methods=["PUT", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def goals_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    if req.method == "PUT":
        response = update_goals(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response, req)

# New routes for enhanced module features

@app.route(route="modules/by-year-semester", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def modules_by_year_semester_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_modules_by_year_semester(req)
    return add_cors_headers(response, req)

@app.route(route="modules/suggestions", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def module_suggestions_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_module_suggestions(req)
    return add_cors_headers(response, req)

# New routes for university-specific features

@app.route(route="university/modules", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def university_modules_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_university_modules(req)
    return add_cors_headers(response, req)

@app.route(route="university/degree-requirements", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def degree_requirements_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_degree_requirements(req)
    return add_cors_headers(response, req)

@app.route(route="university/import-modules", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def import_modules_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = import_template_modules(req)
    return add_cors_headers(response, req)

# New dashboard insights route

@app.route(route="dashboard/insights", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def insights_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_insights(req)
    return add_cors_headers(response, req)


@app.route(route="onboarding/status", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def onboarding_status_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_onboarding_status(req)
    return add_cors_headers(response, req)

@app.route(route="onboarding/save", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def save_onboarding_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = save_onboarding_questionnaire(req)
    return add_cors_headers(response, req)


@app.route(route="modules/analytics", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def module_analytics_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_module_analytics(req)
    return add_cors_headers(response, req)

@app.route(route="logout", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def logout_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = logout_user(req)
    return add_cors_headers(response, req)

# Password reset routes
@app.route(route="password/forgot", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def forgot_password_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = request_password_reset(req)
    return add_cors_headers(response, req)

@app.route(route="password/reset", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def reset_password_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = reset_password(req)
    return add_cors_headers(response, req)

@app.route(route="password/verify-token", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def verify_token_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = verify_token(req)
    return add_cors_headers(response, req)

# Reminder routes
@app.route(route="reminders", methods=["GET", "POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def reminders_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    
    if req.method == "GET":
        response = get_reminders(req)
    elif req.method == "POST":
        response = create_reminder(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )
    
    return add_cors_headers(response, req)

@app.route(route="reminders/{id}", methods=["DELETE", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def reminder_by_id_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    
    if req.method == "DELETE":
        response = delete_reminder(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )
    
    return add_cors_headers(response, req)

@app.route(route="reminders/process", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def process_reminders_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = process_reminders(req)
    return add_cors_headers(response, req)

@app.route(route="reminders/event", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def create_event_reminder_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = create_event_reminder(req)
    return add_cors_headers(response, req)


@app.route(route="study/schedules", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def study_schedules_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_schedules(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/active", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def active_schedule_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_active_schedule_route(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/create", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def create_schedule_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = create_schedule_manual(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/generate", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def generate_schedule_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = create_schedule_ai(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/{id}", methods=["PUT", "DELETE", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def schedule_by_id_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)

    if req.method == "PUT":
        response = update_schedule_route(req)
    elif req.method == "DELETE":
        response = delete_schedule_route(req)
    else:
        response = func.HttpResponse(
            json.dumps({"error": f"Method {req.method} not allowed"}),
            status_code=405,
            mimetype="application/json"
        )

    return add_cors_headers(response, req)

@app.route(route="study/schedules/{id}/activate", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def activate_schedule_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = activate_schedule_route(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/{id}/create-events", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def create_events_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = create_calendar_events_route(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def study_sessions_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_sessions(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions/{id}/start", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def start_session_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = start_session(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions/{id}/complete", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def complete_session_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = complete_session(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions/{id}/reschedule", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def reschedule_session_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = reschedule_session(req)
    return add_cors_headers(response, req)

@app.route(route="study/achievements", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def achievements_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_achievements(req)
    return add_cors_headers(response, req)

@app.route(route="study/streak", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def streak_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_streak(req)
    return add_cors_headers(response, req)

@app.route(route="study/analytics", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def analytics_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_analytics(req)
    return add_cors_headers(response, req)

@app.route(route="study/tips", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def tips_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_tips(req)
    return add_cors_headers(response, req)

@app.route(route="study/tips/{id}/accept", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def accept_tip_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = accept_tip(req)
    return add_cors_headers(response, req)

@app.route(route="study/tips/{id}/reject", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def reject_tip_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = reject_tip(req)
    return add_cors_headers(response, req)


from study_routes import (
    get_current_sessions, get_sidebar_data_route, 
    mark_session_completed, mark_session_missed,
    update_session_statuses
)

# Add these routes to the existing function_app.py routes

@app.route(route="study/sessions/current", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def current_sessions_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_current_sessions(req)
    return add_cors_headers(response, req)

@app.route(route="study/sidebar-data", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def sidebar_data_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_sidebar_data_route(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions/{id}/complete/done", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def mark_session_completed_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = mark_session_completed(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions/{id}/miss", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def mark_session_missed_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = mark_session_missed(req)
    return add_cors_headers(response, req)

@app.route(route="study/sessions/update-statuses", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def update_statuses_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = update_session_statuses(req)
    return add_cors_headers(response, req)

# Also add the timer trigger for the session tracker
@app.schedule(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=True)
def session_tracker_timer(timer: func.TimerRequest) -> None:
    """Timer trigger that runs every 5 minutes to update session statuses"""
    from session_tracker import main as session_tracker_main
    session_tracker_main(timer)


@app.route(route="study/analytics/completion", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def completion_analytics_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_completion_analytics_route(req)
    return add_cors_headers(response, req)

@app.route(route="study/insights/completion", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def completion_insights_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_completion_insights_route(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/{id}/rate", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def rate_schedule_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = rate_ai_schedule(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/analyze-modifications", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def analyze_modifications_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = analyze_schedule_modifications(req)
    return add_cors_headers(response, req)

@app.route(route="study/schedules/{id}/explanations", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def schedule_explanations_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return cors_preflight_response(req)
    response = get_schedule_explanations(req)
    return add_cors_headers(response, req)