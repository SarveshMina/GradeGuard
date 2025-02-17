import os
import json
import datetime
import jwt
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
    get_all_universities_docs
)

JWT_SECRET = os.environ.get("JWT_SECRET", "default_secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

def register_user(req: HttpRequest) -> HttpResponse:
    """
    POST /api/register
    Creates a new user and increments counters for the chosen university/major.
    """
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

    # Validate against Pydantic model
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
        "id": user_in.email,  # using email as the document ID
        "userid": generated_userid,
        "firstName": user_in.firstName,
        "email": user_in.email,
        "password": hashed_password,
        "university": user_in.university,
        "degree": user_in.degree,
        "calcType": user_in.calcType,
        "createdAt": datetime.datetime.utcnow().isoformat()
    }

    # Insert user
    create_user(user_doc)

    # Increment counters
    increment_university_and_major_counter(user_in.university, user_in.degree)

    # Return JWT
    token = create_jwt(user_in.email)
    return HttpResponse(
        json.dumps({"message": "User registered successfully.", "token": token}),
        status_code=201,
        mimetype="application/json"
    )


def login_user(req: HttpRequest) -> HttpResponse:
    """
    POST /api/login
    Logs in an existing user, returns a JWT if successful.
    """
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

    # Check password
    if not bcrypt.verify(user_in.password, user_doc["password"]):
        return HttpResponse(
            json.dumps({"error": "Invalid email or password."}),
            status_code=401,
            mimetype="application/json"
        )

    # Return JWT
    token = create_jwt(user_doc["email"])
    return HttpResponse(
        json.dumps({"message": "Login successful.", "token": token}),
        status_code=200,
        mimetype="application/json"
    )


def create_jwt(email: str) -> str:
    """
    Generate a JWT token with a 1-day expiry.
    """
    payload = {
        "sub": email,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(req: HttpRequest) -> (bool, str):
    """
    Extracts and verifies the JWT from the Authorization header.
    Returns (True, decoded_email) if valid, or (False, error_message) if invalid.
    """
    auth_header = req.headers.get("Authorization")
    if not auth_header:
        return False, "Missing Authorization header"
    if not auth_header.startswith("Bearer "):
        return False, "Authorization header must start with Bearer"
    token = auth_header.split(" ", 1)[1].strip()
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = decoded["sub"]
        return True, email
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"


def protected_resource(req: HttpRequest) -> HttpResponse:
    """
    GET /api/protected
    Example of a protected route that requires a valid JWT.
    """
    is_valid, result = verify_jwt_token(req)
    if not is_valid:
        return HttpResponse(
            json.dumps({"error": result}),
            status_code=401,
            mimetype="application/json"
        )
    email = result
    return HttpResponse(
        json.dumps({"message": f"You are authorized! Token belongs to {email}."}),
        status_code=200,
        mimetype="application/json"
    )


# -------------------------------------------------------------------------
# NEW: GET /api/stats/universities  => returns array of all universities
# -------------------------------------------------------------------------
def get_universities_endpoint(req: HttpRequest) -> HttpResponse:
    """
    GET /api/stats/universities
    Returns an array of docs like:
      [
        {
          "id": "...",
          "name": "...",
          "counter": 123,
          "majors": [ { "major_name": "X", "counter": 10 }, ... ]
        },
        ...
      ]
    """
    try:
        from database import get_all_universities_docs
        docs = get_all_universities_docs()
        return HttpResponse(
            json.dumps(docs),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


# -------------------------------------------------------------------------
# NEW: GET /api/stats/university?name=University%20of%20Southampton
# -------------------------------------------------------------------------
def get_university_endpoint(req: HttpRequest) -> HttpResponse:
    """
    GET /api/stats/university?name=University%20of%20Southampton
    Returns a single doc, e.g.:
      {
        "id": "University of Southampton",
        "name": "University of Southampton",
        "counter": 51,
        "majors": [
          { "major_name": "Computer Science", "counter": 13 },
          ...
        ]
      }
    """
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
        return HttpResponse(
            json.dumps(doc),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def update_calculator_config(req: HttpRequest) -> HttpResponse:
    """
    PUT /api/calculator
    Updates the user's calculator configuration.
    Expects a JSON body matching the CalculatorConfig model.
    Requires a valid JWT in the Authorization header.
    """
    # Verify the JWT token to get the user email
    is_valid, result = verify_jwt_token(req)
    if not is_valid:
        return HttpResponse(
            json.dumps({"error": result}),
            status_code=401,
            mimetype="application/json"
        )
    email = result

    # Parse and validate the request body
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        from models import CalculatorConfig
        config = CalculatorConfig(**body)
    except Exception as e:
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        # Update the user's document with the new calculator config
        from database import update_user_calculator
        update_user_calculator(email, config.dict())
        return HttpResponse(
            json.dumps({"message": "Calculator configuration updated successfully."}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def get_calculator_config(req: HttpRequest) -> HttpResponse:
    """
    GET /api/calculator
    Returns the user's current calculator configuration.
    Requires a valid JWT.
    """
    is_valid, result = verify_jwt_token(req)
    if not is_valid:
        return HttpResponse(
            json.dumps({"error": result}),
            status_code=401,
            mimetype="application/json"
        )
    email = result

    user_doc = get_user_by_email(email)
    if not user_doc:
        return HttpResponse(
            json.dumps({"error": "User not found."}),
            status_code=404,
            mimetype="application/json"
        )
    # Return the calculator configuration if exists, otherwise an empty config
    config = user_doc.get("calculator", {})
    return HttpResponse(
        json.dumps(config),
        status_code=200,
        mimetype="application/json"
    )
