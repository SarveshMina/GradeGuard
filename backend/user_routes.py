# user_routes.py
import os
import json
import datetime
import logging
import jwt
import uuid  # <-- Import uuid module
from passlib.hash import bcrypt
from pydantic import ValidationError
from azure.functions import HttpRequest, HttpResponse

from models import User, UserLogin
from database import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)

JWT_SECRET = os.environ.get("JWT_SECRET", "default_secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

def register_user(req: HttpRequest) -> HttpResponse:
    """
    Endpoint to create a new user.
    Expects JSON matching `User` schema:
        {
          "username": "...",
          "email": "...",
          "password": "..."
        }
    """
    try:
        body = req.get_json()
    except Exception:
        return HttpResponse(
            json.dumps({"error": "Invalid JSON in request body."}),
            status_code=400,
            mimetype="application/json"
        )

    # Validate with Pydantic (userid is now optional)
    try:
        user_in = User(**body)
    except ValidationError as e:
        return HttpResponse(e.json(), status_code=400, mimetype="application/json")

    # Check if email is already in use
    if get_user_by_email(user_in.email):
        return HttpResponse(
            json.dumps({"error": "Email already in use."}),
            status_code=400,
            mimetype="application/json"
        )

    # Check if username is already taken
    if get_user_by_username(user_in.username):
        return HttpResponse(
            json.dumps({"error": "Username already taken."}),
            status_code=400,
            mimetype="application/json"
        )

    # Generate a UUID for the user regardless of what the client provided.
    generated_userid = str(uuid.uuid4())

    # Hash the password before storing
    hashed_password = bcrypt.hash(user_in.password)

    # Build user record for Cosmos DB.
    # Using the email as the 'id' to enable point reads, and our generated UUID as 'userid'.
    user_doc = {
        "id": user_in.email,  # This is the Cosmos DB document ID.
        "userid": generated_userid,
        "username": user_in.username,
        "email": user_in.email,
        "password": hashed_password,
        "createdAt": datetime.datetime.utcnow().isoformat()
    }

    create_user(user_doc)

    # Optionally create JWT so user is "logged in" immediately.
    token = create_jwt(user_in.email)
    return HttpResponse(
        json.dumps({"message": "User registered successfully.", "token": token}),
        status_code=201,
        mimetype="application/json"
    )


def login_user(req: HttpRequest) -> HttpResponse:
    """
    Endpoint to login an existing user.
    Expects JSON matching `UserLogin` schema:
        {
          "email": "...",
          "password": "..."
        }
    """
    try:
        body = req.get_json()
    except:
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

    # Verify password
    if not bcrypt.verify(user_in.password, user_doc["password"]):
        return HttpResponse(
            json.dumps({"error": "Invalid email or password."}),
            status_code=401,
            mimetype="application/json"
        )

    # If valid, create and return a token
    token = create_jwt(user_doc["email"])
    return HttpResponse(
        json.dumps({"message": "Login successful.", "token": token}),
        status_code=200,
        mimetype="application/json"
    )


def create_jwt(email: str) -> str:
    """
    Generate a JWT token with 1-day expiry.
    """
    payload = {
        "sub": email,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(req: HttpRequest) -> (bool, str):
    """
    Extracts and verifies the JWT from 'Authorization' header.
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
    Example of a protected route that requires a valid JWT in `Authorization: Bearer <token>`.
    """
    is_valid, result = verify_jwt_token(req)
    if not is_valid:
        return HttpResponse(json.dumps({"error": result}), status_code=401, mimetype="application/json")

    # If valid, 'result' is the email from the token
    email = result
    return HttpResponse(
        json.dumps({"message": f"You are authorized! Token belongs to {email}."}),
        status_code=200,
        mimetype="application/json"
    )
