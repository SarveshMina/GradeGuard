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
