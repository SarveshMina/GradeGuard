import azure.functions as func
from user_routes import (
    register_user,
    login_user,
    protected_resource,
    get_universities_endpoint,
    get_university_endpoint
)
from google_auth import google_login_redirect, google_auth_callback

app = func.FunctionApp()

# Existing endpoints
@app.route(route="register", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def register_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    return register_user(req)

@app.route(route="login", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def login_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    return login_user(req)

@app.route(route="protected", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def protected_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    return protected_resource(req)

@app.route(route="stats/universities", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_universities(req: func.HttpRequest) -> func.HttpResponse:
    return get_universities_endpoint(req)

@app.route(route="stats/university", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_university(req: func.HttpRequest) -> func.HttpResponse:
    return get_university_endpoint(req)

# Google OAuth endpoints

# Initiates the Google OAuth flow
@app.route(route="auth/google", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def google_login(req: func.HttpRequest) -> func.HttpResponse:
    return google_login_redirect(req)

# Handles the callback from Google after user consent
@app.route(route="auth/google/callback", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def google_callback(req: func.HttpRequest) -> func.HttpResponse:
    return google_auth_callback(req)

@app.route(route="calculator", methods=["PUT"], auth_level=func.AuthLevel.ANONYMOUS)
def update_calculator(req: func.HttpRequest) -> func.HttpResponse:
    return update_calculator_config(req)

@app.route(route="calculator", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_calculator(req: func.HttpRequest) -> func.HttpResponse:
    return get_calculator_config(req)
