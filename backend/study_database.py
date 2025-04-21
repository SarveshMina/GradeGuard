# study_database.py
import uuid
import datetime
import logging
from typing import List, Dict, Any, Optional
from database import _container  


logger = logging.getLogger(__name__)

def create_study_schedule(user_email: str, schedule_data: dict) -> dict:
    """Create a new study schedule"""
    # Generate ID if not provided
    if not schedule_data.get('id'):
        schedule_data['id'] = f"schedule_{str(uuid.uuid4())}"

    # Add metadata
    schedule_data['user_email'] = user_email
    schedule_data['type'] = 'study_schedule'
    now = datetime.datetime.utcnow().isoformat()
    schedule_data['created_at'] = now
    schedule_data['updated_at'] = now
    
    # Initialize events_created flag to track if calendar events have been created
    schedule_data['events_created'] = False
    
    # Handle is_active status (deactivate other schedules if this one is active)
    if schedule_data.get('is_active', False):
        deactivate_all_schedules(user_email)

    # Create in database
    result = _container.create_item(body=schedule_data)
    return result

def get_user_schedules(user_email: str) -> List[dict]:
    """Get all study schedules for a user"""
    query = "SELECT * FROM c WHERE c.type = 'study_schedule' AND c.user_email = @email"
    parameters = [{"name": "@email", "value": user_email}]

    schedules = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return schedules

def get_active_schedule(user_email: str) -> Optional[dict]:
    """Get the active study schedule for a user"""
    query = "SELECT * FROM c WHERE c.type = 'study_schedule' AND c.user_email = @email AND c.is_active = true"
    parameters = [{"name": "@email", "value": user_email}]

    schedules = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    
    return schedules[0] if schedules else None

def get_schedule(user_email: str, schedule_id: str) -> Optional[dict]:
    """Get a specific study schedule"""
    query = "SELECT * FROM c WHERE c.type = 'study_schedule' AND c.id = @id AND c.user_email = @email"
    parameters = [
        {"name": "@id", "value": schedule_id},
        {"name": "@email", "value": user_email}
    ]

    schedules = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    return schedules[0] if schedules else None

def update_schedule(user_email: str, schedule_id: str, updates: dict) -> Optional[dict]:
    """Update a study schedule"""
    schedule = get_schedule(user_email, schedule_id)
    if not schedule:
        return None

    # Ensure schedule is a dictionary before updating it
    if not isinstance(schedule, dict):
        schedule_dict = dict(schedule)
    else:
        schedule_dict = schedule

    # Handle is_active status (deactivate other schedules if this one is being activated)
    if updates.get('is_active', False) and not schedule_dict.get('is_active', False):
        deactivate_all_schedules(user_email)

    # Update fields
    for key, value in updates.items():
        if key not in ['id', 'user_email', 'type', 'created_at']:
            schedule_dict[key] = value

    schedule_dict['updated_at'] = datetime.datetime.utcnow().isoformat()

    # Update in database
    result = _container.replace_item(item=schedule_id, body=schedule_dict)
    return result

def deactivate_all_schedules(user_email: str) -> bool:
    """Deactivate all schedules for a user"""
    query = "SELECT * FROM c WHERE c.type = 'study_schedule' AND c.user_email = @email AND c.is_active = true"
    parameters = [{"name": "@email", "value": user_email}]

    schedules = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    for schedule in schedules:
        schedule['is_active'] = False
        schedule['updated_at'] = datetime.datetime.utcnow().isoformat()
        _container.replace_item(item=schedule['id'], body=schedule)

    return True

def activate_schedule(user_email: str, schedule_id: str) -> Optional[dict]:
    """Activate a specific schedule and deactivate all others"""
    # First deactivate all schedules
    deactivate_all_schedules(user_email)
    
    # Then activate the requested schedule
    schedule = get_schedule(user_email, schedule_id)
    if not schedule:
        return None
    
    # Create a mutable dictionary to modify
    schedule_dict = dict(schedule)
    
    # Update fields
    schedule_dict['is_active'] = True
    schedule_dict['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    # Update in database
    result = _container.replace_item(item=schedule_id, body=schedule_dict)
    return result

def mark_schedule_events_created(user_email: str, schedule_id: str) -> Optional[dict]:
    """Mark that calendar events have been created for this schedule"""
    schedule = get_schedule(user_email, schedule_id)
    if not schedule:
        return None
    
    # Create a mutable dictionary to modify
    schedule_dict = dict(schedule)
    
    # Update fields
    schedule_dict['events_created'] = True
    schedule_dict['updated_at'] = datetime.datetime.utcnow().isoformat()
    
    # Update in database
    result = _container.replace_item(item=schedule_id, body=schedule_dict)
    return result

def delete_schedule(user_email: str, schedule_id: str) -> bool:
    """Delete a study schedule"""
    schedule = get_schedule(user_email, schedule_id)
    if not schedule:
        return False

    # Delete from database
    _container.delete_item(item=schedule_id, partition_key=schedule_id)
    return True

# Study Session Operations

def create_study_session(user_email: str, session_data: dict) -> dict:
    """Create a new study session"""
    # Generate ID if not provided
    if not session_data.get('id'):
        session_data['id'] = f"session_{str(uuid.uuid4())}"

    # Add metadata
    session_data['user_email'] = user_email
    session_data['type'] = 'study_session'

    # Create in database
    result = _container.create_item(body=session_data)
    return result

def get_user_sessions(user_email: str, start_date: Optional[str] = None, end_date: Optional[str] = None, schedule_id: Optional[str] = None) -> List[dict]:
    """Get study sessions for a user with optional date range filtering and schedule filtering"""
    query = "SELECT * FROM c WHERE c.type = 'study_session' AND c.user_email = @email"
    parameters = [{"name": "@email", "value": user_email}]

    if start_date and end_date:
        query += " AND c.date >= @start AND c.date <= @end"
        parameters.extend([
            {"name": "@start", "value": start_date},
            {"name": "@end", "value": end_date}
        ])
        
    if schedule_id:
        query += " AND c.schedule_id = @scheduleId"
        parameters.append({"name": "@scheduleId", "value": schedule_id})

    sessions = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return sessions

def get_active_schedule_sessions(user_email: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    """Get study sessions for a user's active schedule with optional date range filtering"""
    # First get the active schedule
    active_schedule = get_active_schedule(user_email)
    
    if not active_schedule:
        return []
    
    # Convert to dictionary if needed
    active_schedule_dict = dict(active_schedule)
    
    # Then get sessions for that schedule
    return get_user_sessions(user_email, start_date, end_date, active_schedule_dict.get('id'))

def get_session(user_email: str, session_id: str) -> Optional[dict]:
    """Get a specific study session"""
    query = "SELECT * FROM c WHERE c.type = 'study_session' AND c.id = @id AND c.user_email = @email"
    parameters = [
        {"name": "@id", "value": session_id},
        {"name": "@email", "value": user_email}
    ]

    sessions = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    return sessions[0] if sessions else None

def update_session(user_email: str, session_id: str, updates: dict) -> Optional[dict]:
    """Update a study session"""
    session = get_session(user_email, session_id)
    if not session:
        return None

    # Ensure session is a dictionary before updating it
    if not isinstance(session, dict):
        session_dict = dict(session)
    else:
        session_dict = session

    # Update fields
    for key, value in updates.items():
        if key not in ['id', 'user_email', 'type']:
            session_dict[key] = value

    # Update in database
    result = _container.replace_item(item=session_id, body=session_dict)
    return result

def delete_session(user_email: str, session_id: str) -> bool:
    """Delete a study session"""
    session = get_session(user_email, session_id)
    if not session:
        return False

    # Delete from database
    _container.delete_item(item=session_id, partition_key=session_id)
    return True

def delete_sessions_for_schedule(user_email: str, schedule_id: str) -> int:
    """Delete all study sessions associated with a schedule. Returns count of deleted sessions."""
    try:
        # Query for sessions with this schedule_id
        query = """
        SELECT * FROM c
        WHERE c.type = 'study_session'
        AND c.user_email = @email
        AND c.schedule_id = @schedule_id
        """
        parameters = [
            {"name": "@email", "value": user_email},
            {"name": "@schedule_id", "value": schedule_id}
        ]

        sessions = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        # Delete each session
        deleted_count = 0
        for session in sessions:
            _container.delete_item(item=session["id"], partition_key=session["id"])
            deleted_count += 1
            
        return deleted_count
        
    except Exception as e:
        print(f"Error deleting sessions for schedule: {str(e)}")
        return 0

# Study Streak Operations

def get_study_streak(user_email: str) -> dict:
    """Get or create the study streak for a user"""
    query = "SELECT * FROM c WHERE c.type = 'study_streak' AND c.user_email = @email"
    parameters = [{"name": "@email", "value": user_email}]

    streaks = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if streaks:
        return streaks[0]

    # Create new streak document if none exists
    streak_doc = {
        "id": f"streak_{user_email}",
        "user_email": user_email,
        "type": "study_streak",
        "current_streak": 0,
        "longest_streak": 0,
        "last_study_date": None,
        "history": {}
    }

    _container.create_item(body=streak_doc)
    return streak_doc

def update_study_streak(user_email: str, study_date: str, studied: bool) -> dict:
    """Update the study streak based on study activity"""
    streak_doc = get_study_streak(user_email)

    # Ensure streak_doc is a dictionary before updating it
    if not isinstance(streak_doc, dict):
        streak_dict = dict(streak_doc)
    else:
        streak_dict = streak_doc

    # Make sure history exists
    if "history" not in streak_dict:
        streak_dict["history"] = {}

    # Update the history
    streak_dict["history"][study_date] = studied

    if studied:
        # Update last study date
        streak_dict["last_study_date"] = study_date

        # Calculate current streak
        current_date = datetime.datetime.fromisoformat(study_date.replace('Z', '+00:00')).date()

        if streak_dict.get("current_streak", 0) == 0:
            streak_dict["current_streak"] = 1
        else:
            last_study = None
            if streak_dict.get("last_study_date"):
                last_study = datetime.datetime.fromisoformat(
                    streak_dict["last_study_date"].replace('Z', '+00:00')
                ).date()

            if last_study and (current_date - last_study).days <= 1:
                streak_dict["current_streak"] = streak_dict.get("current_streak", 0) + 1
            else:
                streak_dict["current_streak"] = 1

        # Update longest streak if needed
        if streak_dict.get("current_streak", 0) > streak_dict.get("longest_streak", 0):
            streak_dict["longest_streak"] = streak_dict["current_streak"]

    # Save updates
    _container.replace_item(item=streak_dict["id"], body=streak_dict)
    return streak_dict

# Achievements Operations

def get_user_achievements(user_email: str) -> List[dict]:
    """Get all achievements for a user"""
    query = "SELECT * FROM c WHERE c.type = 'achievement' AND c.user_email = @email"
    parameters = [{"name": "@email", "value": user_email}]

    achievements = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if not achievements:
        # Initialize default achievements if none exist
        achievements = initialize_default_achievements(user_email)

    return achievements

def initialize_default_achievements(user_email: str) -> List[dict]:
    """Create default achievements for a new user, including completion-based ones"""
    default_achievements = [
        # Existing achievements
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "First Steps",
            "description": "Complete your first 5 study sessions",
            "category": "consistency",
            "progress": 0,
            "target": 5,
            "progressPercent": 0,
            "status": "in-progress",
            "icon": "/icons/achievement_streak.svg"
        },
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Steady Learner",
            "description": "Maintain a study streak of 7 days",
            "category": "consistency",
            "progress": 0,
            "target": 7,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_streak.svg"
        },
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Time Master",
            "description": "Study for a total of 50 hours",
            "category": "time",
            "progress": 0,
            "target": 50,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_time.svg"
        },
        
        # New completion-based achievements
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Perfect Week",
            "description": "Complete all planned study sessions in a week",
            "category": "completion",
            "progress": 0,
            "target": 1,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_completion.svg"
        },
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Consistency Champion",
            "description": "Maintain 90%+ completion rate for 30 days",
            "category": "completion",
            "progress": 0,
            "target": 30,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_completion.svg"
        },
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Marathon Scholar",
            "description": "Complete 3+ sessions in a single day",
            "category": "completion",
            "progress": 0,
            "target": 1,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_marathon.svg"
        },
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Comeback Kid",
            "description": "Resume studying after breaking a streak",
            "category": "consistency",
            "progress": 0,
            "target": 1,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_comeback.svg"
        }
    ]

    for achievement in default_achievements:
        _container.create_item(body=achievement)

    return default_achievements

def update_achievement(user_email: str, achievement_id: str, progress: int) -> dict:
    """Update an achievement's progress"""
    query = "SELECT * FROM c WHERE c.type = 'achievement' AND c.id = @id AND c.user_email = @email"
    parameters = [
        {"name": "@id", "value": achievement_id},
        {"name": "@email", "value": user_email}
    ]

    achievements = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if not achievements:
        return None

    achievement = achievements[0]

    # Ensure achievement is a dictionary before updating it
    if not isinstance(achievement, dict):
        achievement_dict = dict(achievement)
    else:
        achievement_dict = achievement

    # Update progress
    achievement_dict["progress"] = progress

    # Calculate percentage
    if achievement_dict.get("target", 0) > 0:
        achievement_dict["progressPercent"] = min(100, int((progress / achievement_dict["target"]) * 100))

    # Update status
    if achievement_dict.get("progressPercent", 0) >= 100:
        achievement_dict["status"] = "completed"
    elif achievement_dict.get("status") == "locked" and progress > 0:
        achievement_dict["status"] = "in-progress"

    # Save updates
    _container.replace_item(item=achievement_id, body=achievement_dict)
    return achievement_dict

def check_and_update_achievements(user_email: str) -> List[dict]:
    """Check and update all achievements based on user activity"""
    # First run the existing achievement checks
    achievements = get_user_achievements(user_email)
    
    # Get study statistics
    sessions = get_user_sessions(user_email)
    completed_sessions = [s for s in sessions if s.get("completed", False)]
    
    # Get streak information
    streak_doc = get_study_streak(user_email)
    
    # Calculate total study hours
    total_hours = 0
    for session in completed_sessions:
        if "startTime" in session and "endTime" in session:
            start = datetime.datetime.strptime(session["startTime"], "%H:%M")
            end = datetime.datetime.strptime(session["endTime"], "%H:%M")
            duration = (end - start).total_seconds() / 3600  # Convert to hours
            total_hours += duration
    
    # Calculate weekend sessions
    weekend_sessions = 0
    for session in completed_sessions:
        date_obj = datetime.datetime.fromisoformat(session["date"].replace('Z', '+00:00'))
        if date_obj.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            weekend_sessions += 1
    
    # Update standard achievements
    updated_achievements = []
    
    for achievement in achievements:
        if achievement["name"] == "First Steps":
            update_achievement(user_email, achievement["id"], len(completed_sessions))
        elif achievement["name"] == "Steady Learner":
            update_achievement(user_email, achievement["id"], streak_doc.get("current_streak", 0))
        elif achievement["name"] == "Time Master":
            update_achievement(user_email, achievement["id"], int(total_hours))
        elif achievement["name"] == "Weekend Warrior":
            update_achievement(user_email, achievement["id"], weekend_sessions)
        
        # Fetch the updated achievement
        updated = get_achievement(user_email, achievement["id"])
        updated_achievements.append(updated)
    
    # Now also check completion-based achievements
    completion_achievements = check_and_update_completion_achievements(user_email)
    
    # Merge results, removing duplicates
    achievement_ids = {a["id"] for a in updated_achievements}
    for achievement in completion_achievements:
        if achievement["id"] not in achievement_ids:
            updated_achievements.append(achievement)
    
    return updated_achievements

def get_achievement(user_email: str, achievement_id: str) -> Optional[dict]:
    """Get a specific achievement"""
    query = "SELECT * FROM c WHERE c.type = 'achievement' AND c.id = @id AND c.user_email = @email"
    parameters = [
        {"name": "@id", "value": achievement_id},
        {"name": "@email", "value": user_email}
    ]

    achievements = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    return achievements[0] if achievements else None

# Analytics Operations

def get_study_stats(user_email: str) -> dict:
    """Get or create study statistics for a user"""
    query = "SELECT * FROM c WHERE c.type = 'study_stats' AND c.user_email = @email"
    parameters = [{"name": "@email", "value": user_email}]

    stats_list = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if stats_list:
        return stats_list[0]

    # Create new stats document if none exists
    stats_doc = {
        "id": f"stats_{user_email}",
        "user_email": user_email,
        "type": "study_stats",
        "total_sessions_completed": 0,
        "total_study_hours": 0,
        "completion_rate": 0,
        "avg_productivity_rating": 0,
        "level": 1,
        "total_xp": 0,
        "level_progress_percent": 0,
        "xp_for_next_level": 100,
        "last_updated": datetime.datetime.utcnow().isoformat()
    }

    _container.create_item(body=stats_doc)
    return stats_doc

def update_study_stats(user_email: str) -> dict:
    """Update study statistics based on session history"""
    # Get sessions
    sessions = get_user_sessions(user_email)
    completed_sessions = [s for s in sessions if s.get("completed", False)]

    # Calculate statistics
    total_completed = len(completed_sessions)
    completion_rate = 0
    if sessions:
        completion_rate = int((total_completed / len(sessions)) * 100)

    # Calculate study hours
    total_hours = 0
    for session in completed_sessions:
        if "startTime" in session and "endTime" in session:
            start = datetime.datetime.strptime(session["startTime"], "%H:%M")
            end = datetime.datetime.strptime(session["endTime"], "%H:%M")
            duration = (end - start).total_seconds() / 3600  # Convert to hours
            total_hours += duration

    # Calculate average productivity
    productivity_values = [s.get("productivity", 0) for s in completed_sessions if s.get("productivity")]
    avg_productivity = 0
    if productivity_values:
        avg_productivity = sum(productivity_values) / len(productivity_values)

    # Calculate XP and level
    total_xp = sum(s.get("xpEarned", 0) for s in completed_sessions)

    # Simple leveling system
    level = 1
    xp_for_level = 100  # Base XP for level 1
    remaining_xp = total_xp

    while remaining_xp >= xp_for_level:
        remaining_xp -= xp_for_level
        level += 1
        xp_for_level = int(xp_for_level * 1.5)  # Increase XP needed for each level

    # Calculate progress to next level
    level_progress_percent = int((remaining_xp / xp_for_level) * 100) if xp_for_level > 0 else 0

    # Get or create stats document
    stats_doc = get_study_stats(user_email)

    # Ensure stats_doc is a dictionary before updating it
    if not isinstance(stats_doc, dict):
        stats_dict = dict(stats_doc)
    else:
        stats_dict = stats_doc

    # Update stats
    stats_dict["total_sessions_completed"] = total_completed
    stats_dict["total_study_hours"] = round(total_hours, 1)
    stats_dict["completion_rate"] = completion_rate
    stats_dict["avg_productivity_rating"] = round(avg_productivity, 1)
    stats_dict["level"] = level
    stats_dict["total_xp"] = total_xp
    stats_dict["level_progress_percent"] = level_progress_percent
    stats_dict["xp_for_next_level"] = xp_for_level - remaining_xp
    stats_dict["last_updated"] = datetime.datetime.utcnow().isoformat()

    # Save updates
    _container.replace_item(item=stats_dict["id"], body=stats_dict)
    return stats_dict

# AI Tips Operations

def create_ai_tip(user_email: str, tip_data: dict) -> dict:
    """Create a new AI tip for a user"""
    # Generate ID if not provided
    if not tip_data.get('id'):
        tip_data['id'] = f"tip_{str(uuid.uuid4())}"

    # Add metadata
    tip_data['user_email'] = user_email
    tip_data['type'] = 'ai_tip'
    tip_data['created_at'] = datetime.datetime.utcnow().isoformat()
    tip_data['applied'] = False
    tip_data['rejected'] = False

    # Create in database
    result = _container.create_item(body=tip_data)
    return result

def get_user_ai_tips(user_email: str) -> List[dict]:
    """Get active AI tips for a user"""
    query = """
    SELECT * FROM c
    WHERE c.type = 'ai_tip'
    AND c.user_email = @email
    AND c.applied = false
    AND c.rejected = false
    """
    parameters = [{"name": "@email", "value": user_email}]

    tips = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return tips

def update_ai_tip_status(user_email: str, tip_id: str, applied: bool, rejected: bool) -> Optional[dict]:
    """Update the status of an AI tip (applied or rejected)"""
    query = "SELECT * FROM c WHERE c.type = 'ai_tip' AND c.id = @id AND c.user_email = @email"
    parameters = [
        {"name": "@id", "value": tip_id},
        {"name": "@email", "value": user_email}
    ]

    tips = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if not tips:
        return None

    tip = tips[0]

    # Ensure tip is a dictionary before updating it
    if not isinstance(tip, dict):
        tip_dict = dict(tip)
    else:
        tip_dict = tip

    tip_dict['applied'] = applied
    tip_dict['rejected'] = rejected

    # Save updates
    _container.replace_item(item=tip_dict["id"], body=tip_dict)
    return tip_dict

# Module Analytics Operations

def get_module_study_stats(user_email: str) -> List[dict]:
    """Get study statistics for each module"""
    # Get all modules
    from module_routes import get_user_modules
    modules = get_user_modules(user_email)

    # Get all study sessions
    sessions = get_user_sessions(user_email)

    # Initialize stats for each module
    module_stats = []

    for module in modules:
        module_id = module.get("id")
        module_name = module.get("name")
        module_code = module.get("code", "")

        # Filter sessions for this module
        module_sessions = [s for s in sessions if s.get("module") == module_id]
        completed_sessions = [s for s in module_sessions if s.get("completed", False)]

        # Calculate stats
        total_sessions = len(module_sessions)
        completed_count = len(completed_sessions)
        total_hours = 0

        for session in completed_sessions:
            if "startTime" in session and "endTime" in session:
                start = datetime.datetime.strptime(session["startTime"], "%H:%M")
                end = datetime.datetime.strptime(session["endTime"], "%H:%M")
                duration = (end - start).total_seconds() / 3600  # Convert to hours
                total_hours += duration

        # Calculate weekly average (over the last 4 weeks)
        now = datetime.datetime.utcnow().date()
        four_weeks_ago = now - datetime.timedelta(days=28)
        four_weeks_ago_str = four_weeks_ago.isoformat()

        recent_sessions = [
            s for s in completed_sessions
            if s.get("date") and s.get("date") >= four_weeks_ago_str
        ]

        weekly_hours = 0
        if recent_sessions:
            recent_hours = 0
            for session in recent_sessions:
                if "startTime" in session and "endTime" in session:
                    start = datetime.datetime.strptime(session["startTime"], "%H:%M")
                    end = datetime.datetime.strptime(session["endTime"], "%H:%M")
                    duration = (end - start).total_seconds() / 3600
                    recent_hours += duration

            weekly_hours = recent_hours / 4  # Average over 4 weeks

        # Calculate average productivity
        productivity_values = [s.get("productivity", 0) for s in completed_sessions if s.get("productivity")]
        avg_productivity = 0
        if productivity_values:
            avg_productivity = sum(productivity_values) / len(productivity_values)

        # Calculate progress (simple percentage of completed sessions)
        progress = 0
        if total_sessions > 0:
            progress = int((completed_count / total_sessions) * 100)

        # Create module stats object
        stats = {
            "id": module_id,
            "name": f"{module_name} ({module_code})",
            "sessions": completed_count,
            "hours": round(total_hours, 1),
            "weeklyAvg": round(weekly_hours, 1),
            "productivity": round(avg_productivity, 1),
            "progress": progress
        }

        module_stats.append(stats)

    return module_stats

# Analytics data for charts

def get_module_time_distribution(user_email: str) -> dict:
    """Get time distribution by module for charts"""
    # Get all modules
    from module_routes import get_user_modules
    modules = get_user_modules(user_email)

    # Get all study sessions
    sessions = get_user_sessions(user_email)
    completed_sessions = [s for s in sessions if s.get("completed", False)]

    # Calculate hours per module
    module_hours = {}
    for module in modules:
        module_id = module.get("id")
        module_name = module.get("name")

        # Filter sessions for this module
        module_sessions = [s for s in completed_sessions if s.get("module") == module_id]

        # Calculate total hours
        total_hours = 0
        for session in module_sessions:
            if "startTime" in session and "endTime" in session:
                start = datetime.datetime.strptime(session["startTime"], "%H:%M")
                end = datetime.datetime.strptime(session["endTime"], "%H:%M")
                duration = (end - start).total_seconds() / 3600
                total_hours += duration

        module_hours[module_name] = round(total_hours, 1)

    # Prepare chart data
    labels = list(module_hours.keys())
    data = list(module_hours.values())

    # Generate colors (in a real app, these would be more varied)
    colors = ['#9e78ff', '#ff6b6b', '#4ecdc4', '#ffbe0b', '#8338ec']
    # Make sure we have enough colors
    while len(colors) < len(labels):
        colors.extend(colors[:len(labels)-len(colors)])

    background_colors = colors[:len(labels)]

    chart_data = {
        "labels": labels,
        "datasets": [{
            "data": data,
            "backgroundColor": background_colors
        }]
    }

    return chart_data

def get_sessions_timeline(user_email: str) -> dict:
    """Get study sessions timeline for the last 7 days"""
    # Get current date and date 7 days ago
    now = datetime.datetime.utcnow().date()
    week_ago = now - datetime.timedelta(days=6)  # 7 days including today

    # Generate date range
    date_range = []
    for i in range(7):
        date = week_ago + datetime.timedelta(days=i)
        date_range.append(date)

    # Get all study sessions
    sessions = get_user_sessions(user_email)

    # Count sessions per day
    daily_counts = []
    for date in date_range:
        date_str = date.isoformat()
        count = sum(1 for s in sessions if s.get("date") == date_str)
        daily_counts.append(count)

    # Generate day labels (Mon, Tue, etc.)
    day_labels = [date.strftime('%a') for date in date_range]

    # Prepare chart data
    chart_data = {
        "labels": day_labels,
        "datasets": [{
            "label": "Study Sessions",
            "data": daily_counts,
            "borderColor": "#9e78ff",
            "backgroundColor": "rgba(158, 120, 255, 0.2)",
            "tension": 0.4
        }]
    }

    return chart_data

def get_productivity_patterns(user_email: str) -> dict:
    """Get productivity patterns by time of day"""
    # Get all study sessions
    sessions = get_user_sessions(user_email)
    completed_sessions = [s for s in sessions if s.get("completed", False) and s.get("productivity")]

    # Define time ranges
    time_ranges = [
        {"name": "Morning", "start": "06:00", "end": "12:00"},
        {"name": "Afternoon", "start": "12:00", "end": "17:00"},
        {"name": "Evening", "start": "17:00", "end": "21:00"},
        {"name": "Night", "start": "21:00", "end": "23:59"}
    ]

    # Calculate average productivity for each time range
    productivity_by_time = []

    for time_range in time_ranges:
        range_sessions = []

        for session in completed_sessions:
            if "startTime" in session:
                start_time = session["startTime"]
                if time_range["start"] <= start_time <= time_range["end"]:
                    range_sessions.append(session)

        avg_productivity = 0
        if range_sessions:
            productivity_values = [s.get("productivity", 0) for s in range_sessions]
            avg_productivity = sum(productivity_values) / len(productivity_values)

        productivity_by_time.append({
            "name": time_range["name"],
            "productivity": round(avg_productivity, 1)
        })

    # Prepare chart data
    labels = [item["name"] for item in productivity_by_time]
    data = [item["productivity"] for item in productivity_by_time]

    chart_data = {
        "labels": labels,
        "datasets": [{
            "label": "Productivity",
            "data": data,
            "backgroundColor": "#9e78ff"
        }]
    }

    return chart_data

def get_grade_distribution_data(user_email: str) -> List[dict]:
    """Get grade distribution data for charts"""
    # In a real implementation, this would use actual grade data
    # For this example, we'll return sample data
    return [
        {"name": "0-39%", "range": [0, 39], "count": 1},
        {"name": "40-49%", "range": [40, 49], "count": 2},
        {"name": "50-59%", "range": [50, 59], "count": 3},
        {"name": "60-69%", "range": [60, 69], "count": 4},
        {"name": "70-100%", "range": [70, 100], "count": 5}
    ]


def get_current_and_upcoming_sessions(user_email: str, limit: int = 10) -> List[dict]:
    """Get current and upcoming study sessions for a user's active schedule"""
    # Get current date and time in ISO format
    now = datetime.datetime.utcnow()
    current_date = now.date().isoformat()
    current_time = now.strftime("%H:%M")
    
    # First, try to get the active schedule for the user
    active_schedule = get_active_schedule(user_email)
    
    schedule_filter = ""
    if active_schedule:
        schedule_id = active_schedule.get("id")
        schedule_filter = f"AND c.schedule_id = '{schedule_id}'"
    
    # Build query for upcoming sessions
    # 1. Sessions today that haven't started yet
    # 2. Sessions today that are currently in progress
    # 3. Sessions on future dates
    query = f"""
    SELECT * FROM c 
    WHERE c.type = 'study_session' 
    AND c.user_email = @email
    {schedule_filter}
    AND (
        (c.date = @today AND c.startTime >= @now) OR
        (c.date = @today AND c.startTime <= @now AND c.endTime >= @now) OR
        (c.date > @today)
    )
    AND c.status != 'completed'
    AND c.status != 'missed'
    ORDER BY c.date ASC, c.startTime ASC
    """
    
    parameters = [
        {"name": "@email", "value": user_email},
        {"name": "@today", "value": current_date},
        {"name": "@now", "value": current_time}
    ]
    
    sessions = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True,
        max_item_count=limit
    ))
    
    # Update status for sessions that should be in progress
    for session in sessions:
        if (session.get("date") == current_date and 
            session.get("startTime") <= current_time and 
            session.get("endTime") >= current_time and
            session.get("status") == "planned"):
            
            # Update session to in_progress status
            session["status"] = "in_progress"
            _container.replace_item(item=session["id"], body=session)
    
    return sessions

def get_sessions_requiring_status_update() -> List[dict]:
    """Get sessions that need automatic status updates (missed or in progress)"""
    # Get current date and time in ISO format
    now = datetime.datetime.utcnow()
    current_date = now.date().isoformat()
    current_time = now.strftime("%H:%M")
    
    # Build query to find:
    # 1. Sessions that should be in progress (today, current time between start and end)
    # 2. Sessions that should be marked as missed (end time has passed without completion)
    query = """
    SELECT * FROM c 
    WHERE c.type = 'study_session' 
    AND (
        (c.date = @today AND c.startTime <= @now AND c.endTime >= @now AND c.status = 'planned') OR
        ((c.date < @today OR (c.date = @today AND c.endTime < @now)) AND c.status = 'planned')
    )
    """
    
    parameters = [
        {"name": "@today", "value": current_date},
        {"name": "@now", "value": current_time}
    ]
    
    sessions = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    
    return sessions

def mark_session_as_completed(user_email: str, session_id: str, feedback: Optional[dict] = None) -> Optional[dict]:
    """Mark a session as completed with optional feedback"""
    # Get the session
    session = get_session(user_email, session_id)
    if not session:
        return None
    
    # Ensure session is a dictionary
    if not isinstance(session, dict):
        session_dict = dict(session)
    else:
        session_dict = session
        
    # Update session data
    session_dict["status"] = "completed"
    session_dict["completed"] = True
    session_dict["completed_at"] = datetime.datetime.utcnow().isoformat()
    
    # Add feedback if provided
    if feedback:
        session_dict["productivity"] = feedback.get("productivity")
        session_dict["difficulty"] = feedback.get("difficulty")
        session_dict["feedback_notes"] = feedback.get("notes")
        
        # Add topics if provided
        if "topics" in feedback and feedback["topics"]:
            if not session_dict.get("topics"):
                session_dict["topics"] = []
            session_dict["topics"].extend(feedback["topics"])
            # Remove duplicates while preserving order
            seen = set()
            session_dict["topics"] = [x for x in session_dict["topics"] if not (x in seen or seen.add(x))]
        
        # Calculate XP based on productivity and session duration
        productivity = feedback.get("productivity", 3)
        xp_earned = calculate_xp(session_dict, productivity)
        session_dict["xpEarned"] = xp_earned
    
    # Update session in database
    updated_session = _container.replace_item(item=session_id, body=session_dict)
    
    # Update streak for the user
    current_date = datetime.datetime.utcnow().date().isoformat()
    update_study_streak(user_email, current_date, True)
    
    return updated_session

def mark_session_as_missed(user_email: str, session_id: str) -> Optional[dict]:
    """Mark a session as missed"""
    # Get the session
    session = get_session(user_email, session_id)
    if not session:
        return None
    
    # Ensure session is a dictionary
    if not isinstance(session, dict):
        session_dict = dict(session)
    else:
        session_dict = session
        
    # Update session data
    session_dict["status"] = "missed"
    session_dict["missed"] = True
    
    # Update session in database
    updated_session = _container.replace_item(item=session_id, body=session_dict)
    
    return updated_session

def update_session_statuses_automatically():
    """Automatic update of session statuses based on current time"""
    sessions = get_sessions_requiring_status_update()
    
    now = datetime.datetime.utcnow()
    current_date = now.date().isoformat()
    current_time = now.strftime("%H:%M")
    
    updated_count = 0
    for session in sessions:
        # Check if session should be in progress
        if (session.get("date") == current_date and 
            session.get("startTime") <= current_time and 
            session.get("endTime") >= current_time):
            
            # Update to in_progress
            session["status"] = "in_progress"
            _container.replace_item(item=session["id"], body=session)
            updated_count += 1
            
        # Check if session should be marked as missed
        elif (session.get("date") < current_date or 
              (session.get("date") == current_date and session.get("endTime") < current_time)):
            
            # Mark as missed
            session["status"] = "missed"
            session["missed"] = True
            _container.replace_item(item=session["id"], body=session)
            updated_count += 1
    
    return updated_count

def get_sidebar_data(user_email: str) -> dict:
    """Get data for the sidebar display"""
    # Get active schedule
    active_schedule = get_active_schedule(user_email)
    
    # Get upcoming sessions (limit to 7)
    upcoming_sessions = get_current_and_upcoming_sessions(user_email, 7)
    
    # Get study streak
    streak_data = get_study_streak(user_email)
    
    # Get total sessions and completion rate for active schedule
    schedule_stats = {}
    if active_schedule:
        schedule_id = active_schedule.get("id")
        all_sessions = get_user_sessions(user_email, schedule_id=schedule_id)
        
        total_sessions = len(all_sessions)
        completed_sessions = sum(1 for s in all_sessions if s.get("completed", False))
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        schedule_stats = {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "completion_rate": round(completion_rate, 1)
        }
    
    # Prepare sidebar data
    sidebar_data = {
        "active_schedule": active_schedule,
        "upcoming_sessions": upcoming_sessions,
        "streak": {
            "current_streak": streak_data.get("current_streak", 0),
            "longest_streak": streak_data.get("longest_streak", 0),
            "last_study_date": streak_data.get("last_study_date")
        },
        "schedule_stats": schedule_stats
    }
    
    return sidebar_data

def calculate_xp(session: dict, productivity: int) -> int:
    """Calculate XP earned for a completed session"""
    # Base XP for completing a session
    base_xp = 50

    # Bonus XP based on productivity rating
    productivity_bonus = productivity * 10

    # Time bonus (longer sessions earn more)
    duration_minutes = 0
    if isinstance(session, dict) and "startTime" in session and "endTime" in session:
        start = datetime.datetime.strptime(session["startTime"], "%H:%M")
        end = datetime.datetime.strptime(session["endTime"], "%H:%M")
        duration_minutes = (end - start).total_seconds() / 60

    time_bonus = int(duration_minutes / 30) * 10  # 10 XP per 30 minutes

    total_xp = base_xp + productivity_bonus + time_bonus
    return total_xp


# Enhanced analytics functions to add to study_database.py

def get_completion_analytics(user_email: str) -> dict:
    """Get detailed completion analytics for study sessions"""
    # Get all sessions for the user
    all_sessions = get_user_sessions(user_email)
    
    if not all_sessions:
        return {
            "completion_rate": 0,
            "completion_by_day": {},
            "completion_by_time": {},
            "completion_by_module": {},
            "missed_sessions_count": 0,
            "productivity_by_time": {},
            "completion_trend": []
        }
    
    # Calculate overall completion rate
    total_sessions = len(all_sessions)
    completed_sessions = [s for s in all_sessions if s.get("completed", False)]
    missed_sessions = [s for s in all_sessions if s.get("missed", False) or s.get("status") == "missed"]
    
    completion_rate = (len(completed_sessions) / total_sessions) * 100 if total_sessions > 0 else 0
    
    # Analyze completion by day of week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    completion_by_day = {day: {"total": 0, "completed": 0, "rate": 0} for day in days_of_week}
    
    for session in all_sessions:
        if "date" in session:
            try:
                # Parse date and get day of week
                session_date = datetime.datetime.fromisoformat(session["date"].replace('Z', '+00:00')).date()
                day_of_week = days_of_week[session_date.weekday()]
                
                # Update counts
                completion_by_day[day_of_week]["total"] += 1
                if session.get("completed", False):
                    completion_by_day[day_of_week]["completed"] += 1
                
                # Calculate rate
                day_total = completion_by_day[day_of_week]["total"]
                day_completed = completion_by_day[day_of_week]["completed"]
                completion_by_day[day_of_week]["rate"] = (day_completed / day_total) * 100 if day_total > 0 else 0
            except (ValueError, IndexError):
                continue
    
    # Analyze completion by time of day
    time_periods = ["Morning (6-12)", "Afternoon (12-17)", "Evening (17-21)", "Night (21-6)"]
    completion_by_time = {period: {"total": 0, "completed": 0, "rate": 0} for period in time_periods}
    
    for session in all_sessions:
        if "startTime" in session:
            try:
                # Parse start time
                start_time = datetime.datetime.strptime(session["startTime"], "%H:%M").time()
                hour = start_time.hour
                
                # Determine time period
                if 6 <= hour < 12:
                    period = "Morning (6-12)"
                elif 12 <= hour < 17:
                    period = "Afternoon (12-17)"
                elif 17 <= hour < 21:
                    period = "Evening (17-21)"
                else:
                    period = "Night (21-6)"
                
                # Update counts
                completion_by_time[period]["total"] += 1
                if session.get("completed", False):
                    completion_by_time[period]["completed"] += 1
                
                # Calculate rate
                period_total = completion_by_time[period]["total"]
                period_completed = completion_by_time[period]["completed"]
                completion_by_time[period]["rate"] = (period_completed / period_total) * 100 if period_total > 0 else 0
            except ValueError:
                continue
    
    # Analyze completion by module
    completion_by_module = {}
    modules = {}  # To store module names for later
    
    for session in all_sessions:
        if "module" in session:
            module_id = session["module"]
            
            # Track module name if available
            if "title" in session:
                module_name = session.get("title", "").split(" Study Session")[0]
                modules[module_id] = module_name
            
            # Initialize module stats if needed
            if module_id not in completion_by_module:
                completion_by_module[module_id] = {
                    "name": modules.get(module_id, module_id),
                    "total": 0,
                    "completed": 0,
                    "rate": 0,
                    "avg_productivity": 0
                }
            
            # Update counts
            completion_by_module[module_id]["total"] += 1
            if session.get("completed", False):
                completion_by_module[module_id]["completed"] += 1
                
                # Track productivity if available
                if "productivity" in session and session["productivity"] is not None:
                    if "productivity_sum" not in completion_by_module[module_id]:
                        completion_by_module[module_id]["productivity_sum"] = 0
                        completion_by_module[module_id]["productivity_count"] = 0
                    
                    completion_by_module[module_id]["productivity_sum"] += session["productivity"]
                    completion_by_module[module_id]["productivity_count"] += 1
            
            # Calculate rate and average productivity
            module_total = completion_by_module[module_id]["total"]
            module_completed = completion_by_module[module_id]["completed"]
            completion_by_module[module_id]["rate"] = (module_completed / module_total) * 100 if module_total > 0 else 0
            
            if "productivity_sum" in completion_by_module[module_id] and completion_by_module[module_id]["productivity_count"] > 0:
                completion_by_module[module_id]["avg_productivity"] = (
                    completion_by_module[module_id]["productivity_sum"] / 
                    completion_by_module[module_id]["productivity_count"]
                )
            
            # Remove temporary calculation fields
            if "productivity_sum" in completion_by_module[module_id]:
                del completion_by_module[module_id]["productivity_sum"]
            if "productivity_count" in completion_by_module[module_id]:
                del completion_by_module[module_id]["productivity_count"]
    
    # Calculate productivity by time of day
    productivity_by_time = {period: {"count": 0, "sum": 0, "avg": 0} for period in time_periods}
    
    for session in completed_sessions:
        if "startTime" in session and "productivity" in session and session["productivity"] is not None:
            try:
                # Parse start time
                start_time = datetime.datetime.strptime(session["startTime"], "%H:%M").time()
                hour = start_time.hour
                
                # Determine time period
                if 6 <= hour < 12:
                    period = "Morning (6-12)"
                elif 12 <= hour < 17:
                    period = "Afternoon (12-17)"
                elif 17 <= hour < 21:
                    period = "Evening (17-21)"
                else:
                    period = "Night (21-6)"
                
                # Update productivity stats
                productivity_by_time[period]["count"] += 1
                productivity_by_time[period]["sum"] += session["productivity"]
                
                # Calculate average
                productivity_by_time[period]["avg"] = (
                    productivity_by_time[period]["sum"] / 
                    productivity_by_time[period]["count"]
                )
            except ValueError:
                continue
    
    # Calculate completion trend over time (last 30 days)
    today = datetime.datetime.utcnow().date()
    thirty_days_ago = today - datetime.timedelta(days=30)
    
    # Initialize data for each day
    completion_trend = []
    for i in range(30):
        day = thirty_days_ago + datetime.timedelta(days=i)
        completion_trend.append({
            "date": day.isoformat(),
            "total": 0,
            "completed": 0, 
            "rate": 0
        })
    
    # Map to quickly look up index by date
    date_to_index = {data["date"]: i for i, data in enumerate(completion_trend)}
    
    # Populate with actual data
    for session in all_sessions:
        if "date" in session:
            try:
                session_date = datetime.datetime.fromisoformat(session["date"].replace('Z', '+00:00')).date()
                date_str = session_date.isoformat()
                
                # Only include sessions in the last 30 days
                if date_str in date_to_index:
                    idx = date_to_index[date_str]
                    completion_trend[idx]["total"] += 1
                    if session.get("completed", False):
                        completion_trend[idx]["completed"] += 1
                    
                    # Calculate completion rate
                    day_total = completion_trend[idx]["total"]
                    day_completed = completion_trend[idx]["completed"]
                    completion_trend[idx]["rate"] = (day_completed / day_total) * 100 if day_total > 0 else 0
            except ValueError:
                continue
    
    # Round all rates for readability
    for day in completion_by_day.values():
        day["rate"] = round(day["rate"], 1)
    
    for period in completion_by_time.values():
        period["rate"] = round(period["rate"], 1)
    
    for module in completion_by_module.values():
        module["rate"] = round(module["rate"], 1)
        module["avg_productivity"] = round(module["avg_productivity"], 1)
    
    for period in productivity_by_time.values():
        period["avg"] = round(period["avg"], 1)
    
    for day in completion_trend:
        day["rate"] = round(day["rate"], 1)
    
    return {
        "completion_rate": round(completion_rate, 1),
        "completion_by_day": completion_by_day,
        "completion_by_time": completion_by_time,
        "completion_by_module": completion_by_module,
        "missed_sessions_count": len(missed_sessions),
        "productivity_by_time": productivity_by_time,
        "completion_trend": completion_trend
    }

def generate_completion_insights(user_email: str) -> List[dict]:
    """Generate insights based on session completion patterns"""
    # Get completion analytics
    analytics = get_completion_analytics(user_email)
    
    insights = []
    
    # Insight 1: Overall completion rate
    completion_rate = analytics["completion_rate"]
    if completion_rate >= 90:
        insights.append({
            "type": "positive",
            "title": "Excellent Completion Rate",
            "description": f"Your overall session completion rate of {completion_rate}% is outstanding! Keep up the great work!"
        })
    elif completion_rate >= 75:
        insights.append({
            "type": "positive",
            "title": "Strong Completion Rate",
            "description": f"Your overall session completion rate of {completion_rate}% is good. You're maintaining consistency in your studies."
        })
    elif completion_rate >= 50:
        insights.append({
            "type": "neutral",
            "title": "Moderate Completion Rate",
            "description": f"Your session completion rate is {completion_rate}%. Consider strategies to improve your study consistency."
        })
    else:
        insights.append({
            "type": "warning",
            "title": "Low Completion Rate",
            "description": f"Your session completion rate is {completion_rate}%. Finding ways to prioritize your planned study sessions could help improve your academic performance."
        })
    
    # Insight 2: Best day of the week
    completion_by_day = analytics["completion_by_day"]
    days_with_sessions = {day: data for day, data in completion_by_day.items() if data["total"] >= 3}
    
    if days_with_sessions:
        best_day = max(days_with_sessions.items(), key=lambda x: x[1]["rate"])
        worst_day = min(days_with_sessions.items(), key=lambda x: x[1]["rate"])
        
        if best_day[1]["rate"] >= 75:
            insights.append({
                "type": "positive",
                "title": f"{best_day[0]} is Your Most Productive Day",
                "description": f"You complete {best_day[1]['rate']}% of your study sessions on {best_day[0]}s. Consider scheduling important study sessions on this day."
            })
        
        if worst_day[1]["rate"] <= 50 and worst_day[1]["total"] >= 5:
            insights.append({
                "type": "suggestion",
                "title": f"Struggling on {worst_day[0]}s",
                "description": f"You only complete {worst_day[1]['rate']}% of your sessions on {worst_day[0]}s. Consider rescheduling or finding a different approach for this day."
            })
    
    # Insight 3: Best time of day
    completion_by_time = analytics["completion_by_time"]
    times_with_sessions = {time: data for time, data in completion_by_time.items() if data["total"] >= 3}
    
    if times_with_sessions:
        best_time = max(times_with_sessions.items(), key=lambda x: x[1]["rate"])
        worst_time = min(times_with_sessions.items(), key=lambda x: x[1]["rate"])
        
        if best_time[1]["rate"] >= 75:
            insights.append({
                "type": "positive",
                "title": f"{best_time[0]} is Your Most Effective Time",
                "description": f"You complete {best_time[1]['rate']}% of your study sessions during {best_time[0]}. This appears to be your optimal study time."
            })
        
        if worst_time[1]["rate"] <= 50 and worst_time[1]["total"] >= 5:
            insights.append({
                "type": "suggestion",
                "title": f"Difficulty During {worst_time[0]}",
                "description": f"You only complete {worst_time[1]['rate']}% of your sessions during {worst_time[0]}. Consider scheduling fewer sessions during this time period."
            })
    
    # Insight 4: Module-specific insights
    completion_by_module = analytics["completion_by_module"]
    modules_with_sessions = {module_id: data for module_id, data in completion_by_module.items() if data["total"] >= 3}
    
    if modules_with_sessions:
        # Find module with highest completion rate
        best_module = max(modules_with_sessions.items(), key=lambda x: x[1]["rate"])
        
        # Find module with highest productivity
        productive_modules = {module_id: data for module_id, data in modules_with_sessions.items() if "avg_productivity" in data and data["avg_productivity"] > 0}
        if productive_modules:
            most_productive_module = max(productive_modules.items(), key=lambda x: x[1]["avg_productivity"])
            
            insights.append({
                "type": "positive",
                "title": f"High Productivity in {most_productive_module[1]['name']}",
                "description": f"Your average productivity rating for {most_productive_module[1]['name']} is {most_productive_module[1]['avg_productivity']}/5. This subject seems to engage you well."
            })
        
        # Find module with lowest completion rate
        low_completion_modules = {module_id: data for module_id, data in modules_with_sessions.items() if data["rate"] < 50 and data["total"] >= 5}
        if low_completion_modules:
            worst_module = min(low_completion_modules.items(), key=lambda x: x[1]["rate"])
            
            insights.append({
                "type": "warning",
                "title": f"Struggle with {worst_module[1]['name']}",
                "description": f"You only complete {worst_module[1]['rate']}% of your study sessions for {worst_module[1]['name']}. Consider breaking these sessions into smaller chunks or finding a study partner."
            })
    
    # Insight 5: Missed sessions
    missed_count = analytics["missed_sessions_count"]
    if missed_count >= 10:
        insights.append({
            "type": "warning",
            "title": "High Number of Missed Sessions",
            "description": f"You've missed {missed_count} study sessions. Try setting reminders or adjusting your schedule to better fit your availability."
        })
    
    # Limit to top 5 most relevant insights
    return insights[:5]

def check_and_update_completion_achievements(user_email: str) -> List[dict]:
    """Check and update achievements based on session completion patterns"""
    # Get all user achievements 
    achievements = get_user_achievements(user_email)
    
    # Get all sessions
    sessions = get_user_sessions(user_email)
    
    # Get completed and missed sessions
    completed_sessions = [s for s in sessions if s.get("completed", False)]
    missed_sessions = [s for s in sessions if s.get("missed", False) or s.get("status") == "missed"]
    
    # Calculate completion rate
    total_sessions = len(completed_sessions) + len(missed_sessions)
    completion_rate = (len(completed_sessions) / total_sessions * 100) if total_sessions > 0 else 0
    
    # Check "Perfect Week" achievement
    # Group sessions by week
    sessions_by_week = {}
    today = datetime.datetime.utcnow().date()
    
    for session in sessions:
        if "date" in session:
            try:
                session_date = datetime.datetime.fromisoformat(session["date"].replace('Z', '+00:00')).date()
                # Calculate the start of the week (Monday)
                week_start = session_date - datetime.timedelta(days=session_date.weekday())
                week_key = week_start.isoformat()
                
                # Initialize week data if needed
                if week_key not in sessions_by_week:
                    sessions_by_week[week_key] = {
                        "planned": 0,
                        "completed": 0,
                        "missed": 0
                    }
                
                # Update counts
                if session.get("status") != "rescheduled":  # Don't count rescheduled sessions
                    sessions_by_week[week_key]["planned"] += 1
                    
                    if session.get("completed", False):
                        sessions_by_week[week_key]["completed"] += 1
                    elif session.get("missed", False) or session.get("status") == "missed":
                        sessions_by_week[week_key]["missed"] += 1
            except ValueError:
                continue
    
    # Find weeks with perfect completion (all planned sessions completed)
    perfect_weeks = []
    for week_key, data in sessions_by_week.items():
        if data["planned"] >= 5 and data["completed"] == data["planned"]:
            perfect_weeks.append(week_key)
    
    # Check "Marathon Scholar" achievement (3+ sessions in a single day)
    sessions_by_day = {}
    
    for session in completed_sessions:
        if "date" in session:
            date_key = session["date"]
            if date_key not in sessions_by_day:
                sessions_by_day[date_key] = 0
            sessions_by_day[date_key] += 1
    
    # Find days with 3+ completed sessions
    marathon_days = [day for day, count in sessions_by_day.items() if count >= 3]
    
    # Check "Comeback Kid" achievement
    # This checks if a user has completed a session after breaking a streak of 3+ days
    streak_data = get_study_streak(user_email)
    has_comeback = False
    
    if "history" in streak_data:
        # Convert history to a list of (date, studied) tuples and sort by date
        history = [(datetime.datetime.fromisoformat(date), studied) 
                  for date, studied in streak_data["history"].items()]
        history.sort(key=lambda x: x[0])
        
        # Look for a pattern of 3+ consecutive days of study, then a gap, then resuming
        streak_count = 0
        for i in range(len(history) - 1):
            # If studied on this day
            if history[i][1]:
                streak_count += 1
            else:
                streak_count = 0
                
            # Check if streak was broken and then resumed
            if streak_count >= 3 and i + 1 < len(history):
                # Date difference
                days_diff = (history[i+1][0] - history[i][0]).days
                
                # If there was a gap of 2+ days and then studied again
                if days_diff >= 2 and history[i+1][1]:
                    has_comeback = True
                    break
    
    # Update achievements
    updated_achievements = []
    
    for achievement in achievements:
        if achievement["name"] == "Perfect Week":
            update_achievement(user_email, achievement["id"], len(perfect_weeks))
        elif achievement["name"] == "Consistency Champion":
            # Count days with high completion rate
            high_completion_days = 0
            if completion_rate >= 90 and len(completed_sessions) >= 10:
                high_completion_days = 30  # Simplified for now - in real implementation, would track day by day
            update_achievement(user_email, achievement["id"], high_completion_days)
        elif achievement["name"] == "Marathon Scholar":
            update_achievement(user_email, achievement["id"], 1 if marathon_days else 0)
        elif achievement["name"] == "Comeback Kid":
            update_achievement(user_email, achievement["id"], 1 if has_comeback else 0)
        
        # Fetch the updated achievement
        updated = get_achievement(user_email, achievement["id"])
        updated_achievements.append(updated)
    
    return updated_achievements


def save_ai_schedule_analytics(user_email: str, schedule_id: str, analytics_data: dict) -> bool:
    """Save analytics data for AI-generated schedules"""
    try:
        analytics_doc = {
            "id": f"ai_schedule_analytics_{uuid.uuid4()}",
            "user_email": user_email,
            "schedule_id": schedule_id,
            "type": "ai_schedule_analytics",
            "data": analytics_data,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        
        _container.create_item(body=analytics_doc)
        return True
    except Exception as e:
        logger.error(f"Error saving AI schedule analytics: {str(e)}")
        return False

def get_user_learning_preferences(user_email: str) -> dict:
    """Get learned AI scheduling preferences for a user based on past feedback"""
    try:
        # Query for all feedback records
        query = """
        SELECT * FROM c
        WHERE c.type = 'schedule_feedback'
        AND c.user_email = @email
        ORDER BY c.timestamp DESC
        """
        
        parameters = [{"name": "@email", "value": user_email}]
        
        feedback_records = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        # Extract patterns from feedback
        time_preferences = {}
        day_preferences = {}
        module_preferences = {}
        
        for record in feedback_records:
            feedback_data = record.get("feedback_data", {})
            
            # Extract time preferences for modules
            if "time_preferences" in feedback_data:
                for module_id, times in feedback_data["time_preferences"].items():
                    if module_id not in time_preferences:
                        time_preferences[module_id] = {}
                    
                    for time_slot, count in times.items():
                        if time_slot not in time_preferences[module_id]:
                            time_preferences[module_id][time_slot] = 0
                        
                        time_preferences[module_id][time_slot] += count
            
            # Extract day preferences
            if "day_preferences" in feedback_data:
                for module_id, days in feedback_data["day_preferences"].items():
                    if module_id not in day_preferences:
                        day_preferences[module_id] = {}
                    
                    for day, count in days.items():
                        if day not in day_preferences[module_id]:
                            day_preferences[module_id][day] = 0
                        
                        day_preferences[module_id][day] += count
        
        # Calculate preferred times and days for each module
        for module_id, times in time_preferences.items():
            # Find the most preferred time slot
            preferred_time = max(times.items(), key=lambda x: x[1])[0] if times else None
            
            if module_id not in module_preferences:
                module_preferences[module_id] = {}
            
            module_preferences[module_id]["preferred_time"] = preferred_time
        
        for module_id, days in day_preferences.items():
            # Find the most preferred days
            preferred_days = [day for day, count in sorted(days.items(), key=lambda x: x[1], reverse=True)]
            
            if module_id not in module_preferences:
                module_preferences[module_id] = {}
            
            module_preferences[module_id]["preferred_days"] = preferred_days
        
        return {
            "module_preferences": module_preferences,
            "has_preferences": bool(module_preferences)
        }
    except Exception as e:
        logger.error(f"Error getting user learning preferences: {str(e)}")
        return {"module_preferences": {}, "has_preferences": False}