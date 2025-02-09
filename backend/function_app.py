# function_app.py

import azure.functions as func
from user_routes import register_user, login_user, protected_resource

app = func.FunctionApp()


@app.route(route="register", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def register_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /api/register
      {
        "userid": "some-id",
        "username": "some-user",
        "email": "[email protected]",
        "password": "ValidPassword1!"
      }
    """
    return register_user(req)


@app.route(route="login", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def login_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /api/login
      {
        "email": "[email protected]",
        "password": "ValidPassword1!"
      }
    """
    return login_user(req)


@app.route(route="protected", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def protected_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /api/protected

    Requires a valid JWT in the Authorization header:
      Authorization: Bearer <token>
    """
    return protected_resource(req)
