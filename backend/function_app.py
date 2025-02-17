import azure.functions as func
from user_routes import (
    register_user,
    login_user,
    protected_resource,
    get_universities_endpoint,
    get_university_endpoint
)

app = func.FunctionApp()

@app.route(route="register", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def register_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    return register_user(req)

@app.route(route="login", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def login_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    return login_user(req)

@app.route(route="protected", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def protected_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    return protected_resource(req)

# NEW endpoints for stats
@app.route(route="stats/universities", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_universities(req: func.HttpRequest) -> func.HttpResponse:
    return get_universities_endpoint(req)

@app.route(route="stats/university", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def stats_university(req: func.HttpRequest) -> func.HttpResponse:
    return get_university_endpoint(req)
