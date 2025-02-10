# models.py

import re
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr

class User(BaseModel):
    """
    A single Pydantic model for user data.
    - userid: A unique ID string (could be an email, UUID, or something else). Now optional.
    - username: A unique username in the app.
    - email: Unique email per account (checked at DB level). Must be valid email format.
    - password: Must be 8–20 chars, with at least 1 uppercase, 1 digit, 1 special char.
    """
    userid: Optional[str] = None
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=20)

    @validator("password")
    def validate_password(cls, value):
        # At least one uppercase letter
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter (A-Z).")
        # At least one digit
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit (0-9).")
        # At least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserLogin(BaseModel):
    """
    Minimal model for user login, requiring only email and password.
    """
    email: EmailStr
    password: constr(min_length=8, max_length=20)
