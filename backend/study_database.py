# study_database.py
import uuid
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from database import _container, get_user_by_email
from models import (
    StudyPreferences, 
    ModuleStudyPreference, 
    StudySession,
    StudySessionStatus,
    StudyStreak,
    Achievement,
    AchievementStatus,
    StudyStats
)

# Study Preferences Functions
def get_study_preferences(user_email: str) -> Optional[Dict[str, Any]]:
    """Get a user's study preferences"""
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'study_preferences' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        items = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if items:
            return items[0]
        return None
    except Exception as e:
        print(f"Error getting study preferences: {str(e)}")
        return None

def save_study_preferences(preferences: StudyPreferences) -> Dict[str, Any]:
    """Save or update a user's study preferences"""
    try:
        # Check if preferences already exist
        existing = get_study_preferences(preferences.user_email)
        
        # Prepare document
        preferences_dict = preferences.dict()
        preferences_dict["type"] = "study_preferences"
        
        if existing:
            # Update existing document
            preferences_dict["id"] = existing["id"]
            result = _container.replace_item(item=existing["id"], body=preferences_dict)
        else:
            # Create new document
            preferences_dict["id"] = f"pref_{uuid.uuid4()}"
            result = _container.create_item(body=preferences_dict)
            
        return result
    except Exception as e:
        print(f"Error saving study preferences: {str(e)}")
        raise

# Module Study Preferences Functions
def get_module_study_preferences(user_email: str, module_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get module study preferences for a user, optionally filtered by module_id"""
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'module_study_preference' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        if module_id:
            query += " AND c.module_id = @module_id"
            parameters.append({"name": "@module_id", "value": module_id})
        
        items = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return items
    except Exception as e:
        print(f"Error getting module study preferences: {str(e)}")
        return []

def save_module_study_preference(preference: ModuleStudyPreference, user_email: str) -> Dict[str, Any]:
    """Save or update module study preference"""
    try:
        # Check if preference already exists
        existing = get_module_study_preferences(user_email, preference.module_id)
        
        # Prepare document
        preference_dict = preference.dict()
        preference_dict["type"] = "module_study_preference"
        preference_dict["user_email"] = user_email
        
        if existing:
            # Update existing document
            preference_dict["id"] = existing[0]["id"]
            result = _container.replace_item(item=existing[0]["id"], body=preference_dict)
        else:
            # Create new document
            preference_dict["id"] = f"modpref_{uuid.uuid4()}"
            result = _container.create_item(body=preference_dict)
            
        return result
    except Exception as e:
        print(f"Error saving module study preference: {str(e)}")
        raise

# Study Sessions Functions
def get_study_sessions(
    user_email: str, 
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    module_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get study sessions for a user with optional filters"""
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'study_session' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        if start_date:
            query += " AND c.start_time >= @start_date"
            parameters.append({"name": "@start_date", "value": start_date})
            
        if end_date:
            query += " AND c.start_time <= @end_date"
            parameters.append({"name": "@end_date", "value": end_date})
            
        if status:
            query += " AND c.status = @status"
            parameters.append({"name": "@status", "value": status})
            
        if module_id:
            query += " AND c.module_id = @module_id"
            parameters.append({"name": "@module_id", "value": module_id})
        
        # Order by start time
        query += " ORDER BY c.start_time"
        
        items = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return items
    except Exception as e:
        print(f"Error getting study sessions: {str(e)}")
        return []

def save_study_session(session: StudySession) -> Dict[str, Any]:
    """Save a new study session or update an existing one"""
    try:
        # Prepare document
        session_dict = session.dict(exclude_none=True)
        session_dict["type"] = "study_session"
        
        if not session.id:
            # Create new session
            session_dict["id"] = f"session_{uuid.uuid4()}"
            result = _container.create_item(body=session_dict)
        else:
            # Update existing session
            result = _container.replace_item(item=session.id, body=session_dict)
            
        return result
    except Exception as e:
        print(f"Error saving study session: {str(e)}")
        raise

def update_session_status(
    session_id: str, 
    status: StudySessionStatus,
    productivity_rating: Optional[int] = None,
    difficulty_rating: Optional[int] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Update a study session's status and optional feedback"""
    try:
        # Get the session
        session = _container.read_item(item=session_id, partition_key=session_id)
        
        # Update fields
        session["status"] = status
        
        if productivity_rating is not None:
            session["productivity_rating"] = productivity_rating
            
        if difficulty_rating is not None:
            session["difficulty_rating"] = difficulty_rating
            
        if notes is not None:
            session["notes"] = notes
            
        # Calculate points if session is completed
        if status == StudySessionStatus.COMPLETED:
            points = calculate_session_points(session)
            session["points_earned"] = points
            
            # Update user's study streak
            update_study_streak(session["user_email"])
        
        # Save changes
        result = _container.replace_item(item=session_id, body=session)
        
        # Update study stats if session completed or missed
        if status in [StudySessionStatus.COMPLETED, StudySessionStatus.MISSED]:
            update_study_stats(session["user_email"])
            
        return result
    except Exception as e:
        print(f"Error updating session status: {str(e)}")
        raise

def calculate_session_points(session: Dict[str, Any]) -> int:
    """Calculate points earned for a completed study session"""
    # Base points: 10 per minute
    try:
        start_time = datetime.fromisoformat(session["start_time"].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(session["end_time"].replace('Z', '+00:00'))
        duration_minutes = (end_time - start_time).total_seconds() / 60
        
        base_points = int(duration_minutes * 10)
        
        # Get module preference for difficulty bonus
        module_prefs = get_module_study_preferences(session["user_email"], session["module_id"])
        difficulty_bonus = 0
        assessment_bonus = 0
        
        if module_prefs:
            # Difficult module bonus: +20% for modules rated 4-5 difficulty
            difficulty = module_prefs[0].get("difficulty_rating", 3)
            if difficulty >= 4:
                difficulty_bonus = int(base_points * 0.2)
                
            # Assessment proximity bonus
            assessment_dates = module_prefs[0].get("assessment_dates", [])
            if assessment_dates:
                for assessment_date in assessment_dates:
                    assessment = datetime.fromisoformat(assessment_date.replace('Z', '+00:00'))
                    days_until = (assessment - start_time).days
                    if 0 <= days_until <= 2:  # Within 48 hours
                        assessment_bonus = int(base_points * 0.3)
                        break
        
        # Streak bonus (calculated separately in update_study_streak)
        
        # Calculate total points
        total_points = base_points + difficulty_bonus + assessment_bonus
        
        return total_points
    except Exception as e:
        print(f"Error calculating session points: {str(e)}")
        return 100  # Default fallback

# Streak Management
def get_study_streak(user_email: str) -> Dict[str, Any]:
    """Get a user's study streak information"""
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'study_streak' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        items = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if items:
            return items[0]
            
        # Create new streak document if none exists
        new_streak = {
            "id": f"streak_{uuid.uuid4()}",
            "type": "study_streak",
            "user_email": user_email,
            "current_streak": 0,
            "longest_streak": 0,
            "last_study_date": None,
            "history": {}
        }
        
        return _container.create_item(body=new_streak)
    except Exception as e:
        print(f"Error getting study streak: {str(e)}")
        # Return a default
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "last_study_date": None,
            "history": {}
        }

def update_study_streak(user_email: str) -> Dict[str, Any]:
    """Update a user's study streak based on completed sessions"""
    try:
        # Get the user's streak document
        streak_doc = get_study_streak(user_email)
        
        # Get today's date
        today = datetime.utcnow().date().isoformat()
        
        # Check if we already recorded today
        if today in streak_doc.get("history", {}):
            # Already recorded for today, no need to update
            return streak_doc
            
        # Mark today as completed
        if "history" not in streak_doc:
            streak_doc["history"] = {}
            
        streak_doc["history"][today] = True
        
        # Check if we need to update the streak
        last_date = streak_doc.get("last_study_date")
        current_streak = streak_doc.get("current_streak", 0)
        
        if not last_date:
            # First study session ever
            streak_doc["current_streak"] = 1
            streak_doc["longest_streak"] = 1
        else:
            # Convert to date objects
            last_date_obj = datetime.fromisoformat(last_date).date()
            today_obj = datetime.fromisoformat(today).date()
            
            # Check if consecutive
            if (today_obj - last_date_obj).days == 1:
                # Consecutive day, increase streak
                streak_doc["current_streak"] = current_streak + 1
                
                # Update longest streak if needed
                if streak_doc["current_streak"] > streak_doc.get("longest_streak", 0):
                    streak_doc["longest_streak"] = streak_doc["current_streak"]
            elif (today_obj - last_date_obj).days > 1:
                # Streak broken, reset to 1
                streak_doc["current_streak"] = 1
        
        # Update last study date
        streak_doc["last_study_date"] = today
        
        # Save changes
        result = _container.replace_item(item=streak_doc["id"], body=streak_doc)
        
        # Check for streak achievements
        check_streak_achievements(user_email, streak_doc["current_streak"])
        
        return result
    except Exception as e:
        print(f"Error updating study streak: {str(e)}")
        raise

# Achievements
def get_achievements(user_email: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get achievements for a user, optionally filtered by category"""
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'achievement' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        if category:
            query += " AND c.category = @category"
            parameters.append({"name": "@category", "value": category})
        
        items = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return items
    except Exception as e:
        print(f"Error getting achievements: {str(e)}")
        return []

def create_default_achievements(user_email: str) -> List[Dict[str, Any]]:
    """Create default achievements for a new user"""
    try:
        default_achievements = [
            # Streak achievements
            {
                "name": "First Steps",
                "description": "Complete your first study session",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 100,
                "category": "consistency",
                "badge_icon": "streak_1"
            },
            {
                "name": "Three-Day Streak",
                "description": "Study for 3 consecutive days",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 100,
                "category": "consistency",
                "badge_icon": "streak_3"
            },
            {
                "name": "Week Warrior",
                "description": "Study for 7 consecutive days",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 100,
                "category": "consistency",
                "badge_icon": "streak_7"
            },
            {
                "name": "Consistency Champion",
                "description": "Study for 14 consecutive days",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 100,
                "category": "consistency",
                "badge_icon": "streak_14"
            },
            
            # Time-based achievements
            {
                "name": "Early Bird",
                "description": "Complete 5 study sessions before 9AM",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 5,
                "category": "time",
                "badge_icon": "early_bird"
            },
            {
                "name": "Night Owl",
                "description": "Complete 5 study sessions after 8PM",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 5,
                "category": "time",
                "badge_icon": "night_owl"
            },
            {
                "name": "Weekend Warrior",
                "description": "Complete 5 study sessions on weekends",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 5,
                "category": "time",
                "badge_icon": "weekend_warrior"
            },
            
            # Study achievements
            {
                "name": "Study Starter",
                "description": "Complete 10 study sessions",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 10,
                "category": "study",
                "badge_icon": "study_10"
            },
            {
                "name": "Study Enthusiast",
                "description": "Complete 50 study sessions",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 50,
                "category": "study",
                "badge_icon": "study_50"
            },
            {
                "name": "Study Master",
                "description": "Complete 100 study sessions",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 100,
                "category": "study",
                "badge_icon": "study_100"
            },
            
            # Module achievements
            {
                "name": "Module Maven",
                "description": "Study 10 sessions for a single module",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 10,
                "category": "module",
                "badge_icon": "module_10"
            },
            
            # Hour achievements
            {
                "name": "10 Hour Club",
                "description": "Accumulate 10 hours of study time",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 10,
                "category": "hours",
                "badge_icon": "hours_10"
            },
            {
                "name": "50 Hour Club",
                "description": "Accumulate 50 hours of study time",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 50,
                "category": "hours",
                "badge_icon": "hours_50"
            },
            {
                "name": "Century Club",
                "description": "Accumulate 100 hours of study time",
                "status": AchievementStatus.LOCKED,
                "progress": 0,
                "target": 100,
                "category": "hours",
                "badge_icon": "hours_100"
            }
        ]
        
        # Save each achievement
        results = []
        for achievement in default_achievements:
            # Add common fields
            achievement["id"] = f"achievement_{uuid.uuid4()}"
            achievement["user_email"] = user_email
            achievement["type"] = "achievement"
            
            # Create in database
            result = _container.create_item(body=achievement)
            results.append(result)
            
        return results
    except Exception as e:
        print(f"Error creating default achievements: {str(e)}")
        raise

def update_achievement_progress(
    user_email: str, 
    achievement_id: str, 
    progress: int,
    unlock: bool = False
) -> Dict[str, Any]:
    """Update an achievement's progress and status"""
    try:
        # Get the achievement
        achievement = _container.read_item(item=achievement_id, partition_key=achievement_id)
        
        # Update progress
        achievement["progress"] = progress
        
        # Update status if unlocking or reaching 100%
        if unlock and achievement["status"] == AchievementStatus.LOCKED:
            achievement["status"] = AchievementStatus.UNLOCKED
            achievement["unlocked_date"] = datetime.utcnow().isoformat()
            
        if progress >= achievement["target"] and achievement["status"] != AchievementStatus.COMPLETED:
            achievement["status"] = AchievementStatus.COMPLETED
            achievement["completed_date"] = datetime.utcnow().isoformat()
            
            # Calculate percentage progress
            achievement["progress"] = achievement["target"]
            
        # Calculate percentage progress for UI
        if "progress_percent" not in achievement:
            percent = min(100, int((progress / achievement["target"]) * 100))
            achievement["progress_percent"] = percent
            
        # Save changes
        result = _container.replace_item(item=achievement_id, body=achievement)
        return result
    except Exception as e:
        print(f"Error updating achievement progress: {str(e)}")
        raise

def check_streak_achievements(user_email: str, current_streak: int) -> None:
    """Check and update streak-based achievements"""
    try:
        # Get all achievements for the user
        achievements = get_achievements(user_email, "consistency")
        
        # Define streak thresholds to check
        streak_achievements = {
            "First Steps": 1,
            "Three-Day Streak": 3,
            "Week Warrior": 7,
            "Consistency Champion": 14
        }
        
        # Update applicable achievements
        for achievement in achievements:
            name = achievement.get("name")
            if name in streak_achievements and current_streak >= streak_achievements[name]:
                # This streak achievement should be completed
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    achievement["target"], # Set to target to complete it
                    unlock=True
                )
    except Exception as e:
        print(f"Error checking streak achievements: {str(e)}")

def check_time_based_achievements(user_email: str) -> None:
    """Check and update time-based achievements (early bird, night owl, weekend)"""
    try:
        # Get all time-based achievements
        achievements = get_achievements(user_email, "time")
        
        # Get completed sessions
        completed_sessions = get_study_sessions(
            user_email, 
            status=StudySessionStatus.COMPLETED
        )
        
        # Count early bird sessions (before 9AM)
        early_bird_count = 0
        # Count night owl sessions (after 8PM)
        night_owl_count = 0
        # Count weekend sessions
        weekend_count = 0
        
        for session in completed_sessions:
            start_time = datetime.fromisoformat(session["start_time"].replace('Z', '+00:00'))
            
            # Early bird check
            if start_time.hour < 9:
                early_bird_count += 1
                
            # Night owl check
            if start_time.hour >= 20:
                night_owl_count += 1
                
            # Weekend check
            if start_time.weekday() >= 5:  # 5=Saturday, 6=Sunday
                weekend_count += 1
        
        # Update achievements
        for achievement in achievements:
            name = achievement.get("name")
            
            if name == "Early Bird":
                progress = min(achievement["target"], early_bird_count)
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    progress,
                    unlock=(progress > 0)
                )
            elif name == "Night Owl":
                progress = min(achievement["target"], night_owl_count)
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    progress,
                    unlock=(progress > 0)
                )
            elif name == "Weekend Warrior":
                progress = min(achievement["target"], weekend_count)
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    progress,
                    unlock=(progress > 0)
                )
    except Exception as e:
        print(f"Error checking time-based achievements: {str(e)}")

def check_study_count_achievements(user_email: str, count: int) -> None:
    """Check and update achievements based on total completed study sessions"""
    try:
        # Get all study count achievements
        achievements = get_achievements(user_email, "study")
        
        # Update applicable achievements
        for achievement in achievements:
            name = achievement.get("name")
            target = achievement.get("target", 0)
            
            if count >= target:
                # This achievement should be completed
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    target, # Set to target to complete it
                    unlock=True
                )
            elif count > 0:
                # Update progress
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    count,
                    unlock=True
                )
    except Exception as e:
        print(f"Error checking study count achievements: {str(e)}")

def check_hour_achievements(user_email: str, total_hours: float) -> None:
    """Check and update achievements based on total study hours"""
    try:
        # Get all hour achievements
        achievements = get_achievements(user_email, "hours")
        
        # Update applicable achievements
        for achievement in achievements:
            name = achievement.get("name")
            target = achievement.get("target", 0)
            
            if total_hours >= target:
                # This achievement should be completed
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    target, # Set to target to complete it
                    unlock=True
                )
            elif total_hours > 0:
                # Update progress
                update_achievement_progress(
                    user_email,
                    achievement["id"],
                    int(total_hours),
                    unlock=True
                )
    except Exception as e:
        print(f"Error checking hour achievements: {str(e)}")

# Study Stats
def get_study_stats(user_email: str) -> Dict[str, Any]:
    """Get a user's study statistics"""
    try:
        query = """
        SELECT * FROM c 
        WHERE c.type = 'study_stats' 
        AND c.user_email = @email
        """
        parameters = [{"name": "@email", "value": user_email}]
        
        items = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if items:
            return items[0]
            
        # Create new stats document if none exists
        new_stats = {
            "id": f"stats_{uuid.uuid4()}",
            "type": "study_stats",
            "user_email": user_email,
            "total_sessions_planned": 0,
            "total_sessions_completed": 0,
            "total_study_time_minutes": 0,
            "avg_productivity_rating": 0.0,
            "most_studied_module": None,
            "level": 1,
            "total_xp": 0,
            "modules_stats": {},
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return _container.create_item(body=new_stats)
    except Exception as e:
        print(f"Error getting study stats: {str(e)}")
        # Return a default
        return {
            "total_sessions_planned": 0,
            "total_sessions_completed": 0,
            "total_study_time_minutes": 0,
            "avg_productivity_rating": 0.0,
            "level": 1,
            "total_xp": 0
        }

def update_study_stats(user_email: str) -> Dict[str, Any]:
    """Update a user's study statistics"""
    try:
        # Get the user's stats document
        stats_doc = get_study_stats(user_email)
        
        # Get all sessions
        all_sessions = get_study_sessions(user_email)
        completed_sessions = [s for s in all_sessions if s.get("status") == "completed"]
        
        # Calculate stats
        total_planned = len(all_sessions)
        total_completed = len(completed_sessions)
        
        # Calculate total study time
        total_minutes = 0
        module_minutes = {}
        productivity_ratings = []
        points_earned = 0
        
        for session in completed_sessions:
            try:
                start_time = datetime.fromisoformat(session["start_time"].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(session["end_time"].replace('Z', '+00:00'))
                duration = (end_time - start_time).total_seconds() / 60
                
                total_minutes += duration
                
                # Track by module
                module_id = session.get("module_id")
                if module_id:
                    if module_id not in module_minutes:
                        module_minutes[module_id] = 0
                    module_minutes[module_id] += duration
                
                # Track productivity ratings
                if "productivity_rating" in session and session["productivity_rating"] is not None:
                    productivity_ratings.append(session["productivity_rating"])
                    
                # Track points earned
                if "points_earned" in session and session["points_earned"] is not None:
                    points_earned += session["points_earned"]
            except:
                continue
        
        # Find most studied module
        most_studied_module = None
        most_minutes = 0
        
        for module_id, minutes in module_minutes.items():
            if minutes > most_minutes:
                most_minutes = minutes
                most_studied_module = module_id
        
        # Calculate average productivity rating
        avg_productivity = 0
        if productivity_ratings:
            avg_productivity = sum(productivity_ratings) / len(productivity_ratings)
        
        # Update stats document
        stats_doc["total_sessions_planned"] = total_planned
        stats_doc["total_sessions_completed"] = total_completed
        stats_doc["total_study_time_minutes"] = total_minutes
        stats_doc["avg_productivity_rating"] = round(avg_productivity, 1)
        stats_doc["most_studied_module"] = most_studied_module
        
        # Prepare module stats
        module_stats = {}
        for module_id, minutes in module_minutes.items():
            module_sessions = [s for s in completed_sessions if s.get("module_id") == module_id]
            module_productivity = [s.get("productivity_rating", 0) for s in module_sessions if "productivity_rating" in s and s["productivity_rating"] is not None]
            
            avg_module_productivity = 0
            if module_productivity:
                avg_module_productivity = sum(module_productivity) / len(module_productivity)
            
            module_stats[module_id] = {
                "total_sessions": len(module_sessions),
                "total_minutes": minutes,
                "avg_productivity": round(avg_module_productivity, 1)
            }
        
        stats_doc["modules_stats"] = module_stats
        
        # Update XP and check level
        current_xp = stats_doc.get("total_xp", 0)
        new_xp = current_xp + points_earned
        stats_doc["total_xp"] = new_xp
        
        # Check for level up
        current_level = stats_doc.get("level", 1)
        new_level = calculate_level(new_xp)
        
        if new_level > current_level:
            stats_doc["level"] = new_level
            # TODO: Send notification about level up
        
        # Update last_updated
        stats_doc["last_updated"] = datetime.utcnow().isoformat()
        
        # Save changes
        result = _container.replace_item(item=stats_doc["id"], body=stats_doc)
        
        # Check achievements
        check_study_count_achievements(user_email, total_completed)
        check_hour_achievements(user_email, total_minutes / 60)  # Convert to hours
        check_time_based_achievements(user_email)
        
        return result
    except Exception as e:
        print(f"Error updating study stats: {str(e)}")
        raise

def calculate_level(xp: int) -> int:
    """Calculate user level based on XP"""
    # Define XP thresholds for each level
    level_thresholds = [
        0,       # Level 1: 0 XP
        1000,    # Level 2: 1,000 XP
        2500,    # Level 3: 2,500 XP
        5000,    # Level 4: 5,000 XP
        10000,   # Level 5: 10,000 XP
        17500,   # Level 6: 17,500 XP
        27500,   # Level 7: 27,500 XP
        40000,   # Level 8: 40,000 XP
        55000,   # Level 9: 55,000 XP
        75000,   # Level 10: 75,000 XP
        100000,  # Level 11: 100,000 XP
        130000,  # Level 12: 130,000 XP
        165000,  # Level 13: 165,000 XP
        205000,  # Level 14: 205,000 XP
        250000,  # Level 15: 250,000 XP
        300000,  # Level 16: 300,000 XP
        355000,  # Level 17: 355,000 XP
        415000,  # Level 18: 415,000 XP
        480000,  # Level 19: 480,000 XP
        550000   # Level 20: 550,000 XP
    ]
    
    # Find the highest level where XP is above the threshold
    level = 1
    for i, threshold in enumerate(level_thresholds):
        if xp >= threshold:
            level = i + 1
        else:
            break
            
    return level