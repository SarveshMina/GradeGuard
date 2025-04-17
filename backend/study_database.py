# study_database.py
import uuid
import datetime
from typing import List, Dict, Any, Optional  # Added missing imports
from database import _container  # Import the CosmosDB container from your existing database.py

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

    # Update fields
    for key, value in updates.items():
        if key not in ['id', 'user_email', 'type', 'created_at']:
            schedule_dict[key] = value

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

def get_user_sessions(user_email: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    """Get study sessions for a user with optional date range filtering"""
    query = "SELECT * FROM c WHERE c.type = 'study_session' AND c.user_email = @email"
    parameters = [{"name": "@email", "value": user_email}]

    if start_date and end_date:
        query += " AND c.date >= @start AND c.date <= @end"
        parameters.extend([
            {"name": "@start", "value": start_date},
            {"name": "@end", "value": end_date}
        ])

    sessions = list(_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return sessions

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
    """Create default achievements for a new user"""
    default_achievements = [
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
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Perfect Week",
            "description": "Complete all planned study sessions in a week",
            "category": "consistency",
            "progress": 0,
            "target": 1,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_mastery.svg"
        },
        {
            "id": f"ach_{uuid.uuid4()}",
            "user_email": user_email,
            "type": "achievement",
            "name": "Weekend Warrior",
            "description": "Complete 10 study sessions on weekends",
            "category": "consistency",
            "progress": 0,
            "target": 10,
            "progressPercent": 0,
            "status": "locked",
            "icon": "/icons/achievement_locked.svg"
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
    """Check and update achievements based on user activity"""
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

    # Update achievements
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