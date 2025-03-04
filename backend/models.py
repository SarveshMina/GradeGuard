# models.py

import re
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator, constr, conint, confloat

class YearSetting(BaseModel):
    year: str
    active: bool = True
    credits: conint(ge=0)
    weight: confloat(ge=0, le=100)

class CalculatorConfig(BaseModel):
    years: List[YearSetting]

class User(BaseModel):
    userid: Optional[str] = None
    firstName: str
    email: EmailStr
    password: str
    university: str
    degree: str
    calcType: str
    calculator: Optional[CalculatorConfig] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

    @field_validator("calcType")
    @classmethod
    def validate_calc_type(cls, value):
        allowed = ["UK Percentage", "US GPA 4.0", "US GPA 5.0"]
        if value not in allowed:
            raise ValueError("calcType must be one of: " + ", ".join(allowed))
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=20)

class CalendarEvent(BaseModel):
    id: Optional[str] = None
    user_email: str
    title: str
    description: Optional[str] = None
    date: str  # ISO format date
    start_time: Optional[str] = None  # For time-specific events
    end_time: Optional[str] = None
    all_day: bool = True
    type: str = "general"  # e.g., "assignment", "exam", "study"
    color: Optional[str] = None  # Color code for the event
    completed: bool = False

class UserProfileUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    avatar: Optional[str] = None
    dateOfBirth: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must have at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must have at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must have at least one special character")
        return value

class UserSettings(BaseModel):
    dark_mode: Optional[bool] = False
    notifications_enabled: Optional[bool] = True
    calendar_view: Optional[str] = "month"
    language: Optional[str] = "en"