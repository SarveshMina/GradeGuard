import re
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator, constr, conint, confloat

class YearSetting(BaseModel):
    year: str          # e.g., "Year 1", "Year 2", etc. or "Masters"
    active: bool = True
    credits: conint(ge=0)  # number of credits, minimum 0
    weight: confloat(ge=0, le=100)  # percentage weight (0-100)

class CalculatorConfig(BaseModel):
    years: List[YearSetting]

class User(BaseModel):
    """
    Model for new user data.
    Fields:
      - firstName: The user's first name.
      - email: The user's email address.
      - password: Must be 8–20 characters with at least one uppercase letter, one digit, and one special character.
      - university: The university or college name.
      - degree: The degree the user is pursuing.
      - calcType: Must be one of: "UK Percentage", "US GPA 4.0", "US GPA 5.0".
    """
    userid: Optional[str] = None
    firstName: str
    email: EmailStr
    password: constr(min_length=8, max_length=20)
    university: str
    degree: str
    calcType: str
    calcType: str
    # Add the calculator configuration as an optional field
    calculator: CalculatorConfig = None

    @validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter (A-Z).")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit (0-9).")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

    @validator("calcType")
    def validate_calc_type(cls, value):
        allowed = ["UK Percentage", "US GPA 4.0", "US GPA 5.0"]
        if value not in allowed:
            raise ValueError("Calculator type must be one of: " + ", ".join(allowed))
        return value


class UserLogin(BaseModel):
    """
    Model for user login data.
    """
    email: EmailStr
    password: constr(min_length=8, max_length=20)