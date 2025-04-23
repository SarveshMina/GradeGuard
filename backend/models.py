# models.py

import re
from pydantic import BaseModel, EmailStr, field_validator, constr, conint, confloat, Field
from typing import Dict, List, Optional, Any, Union
from datetime import time, date, datetime
from enum import Enum

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

class AppearanceSettings(BaseModel):
    accentColor: Optional[str] = "purple"
    fontSize: Optional[str] = "medium"
    highContrast: Optional[bool] = False

class AcademicSettings(BaseModel):
    gradingScale: Optional[List[dict]] = None
    termStartDate: Optional[str] = None
    termEndDate: Optional[str] = None
    holidays: Optional[List[dict]] = None

class AccessibilitySettings(BaseModel):
    screenReaderOptimized: Optional[bool] = False
    keyboardShortcuts: Optional[bool] = True
    focusMode: Optional[bool] = False

class CalendarSettings(BaseModel):
    firstDayOfWeek: Optional[str] = "sunday"
    defaultEventDuration: Optional[str] = "60"
    defaultEventType: Optional[str] = "general"
    timeFormat: Optional[str] = "12h"
    dateFormat: Optional[str] = "MM/DD/YYYY"


class UserSettings(BaseModel):
    dark_mode: Optional[bool] = False
    notifications_enabled: Optional[bool] = True
    calendar_view: Optional[str] = "month"
    language: Optional[str] = "en"
    appearance: Optional[AppearanceSettings] = None
    academic: Optional[AcademicSettings] = None
    accessibility: Optional[AccessibilitySettings] = None
    calendar: Optional[CalendarSettings] = None

class Assessment(BaseModel):
    name: str
    weight: confloat(ge=0, le=100)
    score: confloat(ge=0, le=100)

class Examination(BaseModel):
    name: str = "Final Examination"
    weight: confloat(ge=0, le=100)
    score: confloat(ge=0, le=100)

class Module(BaseModel):
    id: Optional[str] = None
    user_email: str
    name: str
    code: Optional[str] = None
    credits: confloat(ge=0)
    year: str  # e.g., "Year 1"
    semester: int = 1  # Added semester field, default to 1
    score: confloat(ge=0, le=100)
    assessments: List[Assessment] = []
    examination: Optional[Examination] = None
    university: Optional[str] = None  # University name
    degree: Optional[str] = None      # Degree/major name
    description: Optional[str] = None  # Module description
    completed: bool = False           # Whether the module is completed
    status: str = "active"            # Status of the module: active, completed, dropped

    class Config:
        extra = "allow"  # Allow extra fields

class GradeTarget(BaseModel):
    title: str
    description: str
    target_score: confloat(ge=0, le=100)
    progress: confloat(ge=0, le=100)

class Activity(BaseModel):
    type: str  # Type of activity: grade, submission, etc.
    title: str
    description: str
    time: str

class UserDashboardConfig(BaseModel):
    view_preferences: Optional[dict] = None
    recent_activities: Optional[List[Activity]] = None
    goals: Optional[List[GradeTarget]] = None
    grade_visualization: Optional[dict] = None

class EducationDetails(BaseModel):
    level: str  # Undergraduate, Postgraduate, etc.
    mode: str  # Full-time, Part-time
    studyTimes: List[str] = []  # Morning, Afternoon, Evening

class YearWeight(BaseModel):
    year: str
    weight: float


class DegreeStructure(BaseModel):
    totalYears: int
    semestersPerYear: int
    creditsPerYear: int
    currentYear: str
    yearWeights: Dict[str, float]
    degreeType: str = "UK Percentage"
    targetGrade: Optional[float] = 70



class OnboardingQuestionnaire(BaseModel):
    educationDetails: Optional[EducationDetails] = None
    degreeStructure: Optional[DegreeStructure] = None

from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class TimeOfDay(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"



class StudySchedule(BaseModel):
    id: str
    user_email: str
    name: str
    start_date: str  # ISO format date
    end_date: str    # ISO format date
    preferred_times: List[TimeOfDay]
    available_days: List[DayOfWeek]
    session_duration: int  # minutes
    break_duration: int    # minutes
    max_sessions_per_day: int
    modules: List[str]    # List of module IDs
    created_at: str       # ISO format datetime
    updated_at: str       # ISO format datetime
    is_ai_generated: bool = False
    is_active: bool = False
    events_created: bool = False

    class Config:
        extra = "allow"


class StudySessionStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    RESCHEDULED = "rescheduled"

class StudySession(BaseModel):
    id: str
    user_email: str
    title: str
    module: str
    date: str  # ISO format date
    startTime: str
    endTime: str
    description: Optional[str] = None
    topics: Optional[List[str]] = None
    status: StudySessionStatus = StudySessionStatus.PLANNED
    completed: bool = False
    missed: bool = False
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    productivity: Optional[int] = None  # 1-5 rating
    difficulty: Optional[int] = None    # 1-5 rating
    feedback_notes: Optional[str] = None
    xpEarned: Optional[int] = None
    notes: Optional[str] = None
    event_id: Optional[str] = None  # Reference to calendar event
    schedule_id: Optional[str] = None  # Reference to parent schedule
    reminder_sent: bool = False
    
    class Config:
        extra = "allow"


class SessionFeedback(BaseModel):
    productivity: int = Field(ge=1, le=5)
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    topics: List[str] = []
    
    class Config:
        extra = "allow"

class StudyStreak(BaseModel):
    user_email: str
    current_streak: int = 0
    longest_streak: int = 0
    last_study_date: Optional[str] = None  # ISO format date
    history: Dict[str, bool] = Field(default_factory=dict)  # Date -> studied

    class Config:
        extra = "allow"


class AchievementStatus(str, Enum):
    LOCKED = "locked"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class Achievement(BaseModel):
    id: str
    name: str
    description: str
    category: str  # consistency, time, mastery
    progress: int
    target: int
    progressPercent: int
    status: AchievementStatus
    icon: Optional[str] = None

    class Config:
        extra = "allow"


class StudyStats(BaseModel):
    user_email: str
    total_sessions_completed: int = 0
    total_study_hours: float = 0
    completion_rate: int = 0
    avg_productivity_rating: float = 0
    level: int = 1
    total_xp: int = 0
    level_progress_percent: int = 0
    xp_for_next_level: int = 100
    
    class Config:
        extra = "allow"


class AiTip(BaseModel):
    id: str
    user_email: str
    title: str
    text: str
    created_at: str  # ISO format datetime
    applied: bool = False
    rejected: bool = False

    class Config:
        extra = "allow"


class ScheduleRequest(BaseModel):
    name: str
    start_date: str
    end_date: str
    preferred_times: List[str]
    available_days: List[str]
    session_duration: int
    break_duration: int
    max_sessions_per_day: int
    modules: List[str]
    is_active: Optional[bool] = True

    class Config:
        extra = "allow"


class FeedbackForm(BaseModel):
    productivity: int
    difficulty: int
    notes: Optional[str] = None
    topics: List[str] = []

    class Config:
        extra = "allow"


class ScheduleActivationRequest(BaseModel):
    schedule_id: str

    class Config:
        extra = "allow"

class ModuleReview(BaseModel):
    id: Optional[str] = None
    module_id: str
    user_email: str
    university: str
    degree: str
    difficulty_rating: conint(ge=1, le=5)
    teaching_quality_rating: conint(ge=1, le=5)
    recommended_rating: conint(ge=1, le=5)
    comment: Optional[str] = None
    semester: Optional[int] = None
    year: Optional[str] = None
    grade_received: Optional[int] = None
    anonymous: bool = True
    created_at: Optional[str] = None

class ModuleStatistics(BaseModel):
    difficulty_avg: float = 0.0
    teaching_quality_avg: float = 0.0
    recommended_avg: float = 0.0
    total_reviews: int = 0
    grade_distribution: dict = {}
    
class ModuleWithStatistics(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    university: str
    degree: str
    credits: Optional[int] = None
    year: Optional[str] = None
    semester: Optional[int] = None
    students_count: int = 0
    average_score: float = 0.0
    statistics: ModuleStatistics = None