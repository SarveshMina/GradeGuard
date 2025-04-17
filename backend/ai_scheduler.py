# ai_scheduler.py
import os
import json
import datetime
import uuid
from typing import List, Dict, Any
import openai
from openai import OpenAI

# Configure OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
client = None

if api_key:
    client = OpenAI(api_key=api_key)

def generate_study_schedule(user_email: str, schedule_request: dict, modules: List[dict]) -> tuple:
    """Generate an optimized study schedule using AI"""
    # Prepare the context with user preferences and modules
    context = {
        "preferences": {
            "start_date": schedule_request.get("start_date"),
            "end_date": schedule_request.get("end_date"),
            "preferred_times": schedule_request.get("preferred_times", []),
            "available_days": schedule_request.get("available_days", []),
            "session_duration": schedule_request.get("session_duration", 60),
            "break_duration": schedule_request.get("break_duration", 15),
            "max_sessions_per_day": schedule_request.get("max_sessions_per_day", 3)
        },
        "modules": [
            {
                "id": module.get("id"),
                "name": module.get("name"),
                "code": module.get("code", ""),
                "credits": module.get("credits", 0),
                "difficulty": calculate_module_difficulty(module)
            }
            for module in modules
        ]
    }
    
    # Generate date range
    start_date = datetime.datetime.fromisoformat(schedule_request["start_date"].replace('Z', '+00:00')).date()
    end_date = datetime.datetime.fromisoformat(schedule_request["end_date"].replace('Z', '+00:00')).date()
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date.isoformat())
        current_date += datetime.timedelta(days=1)
    
    # Create the prompt for the AI
    prompt = f"""
    You are an AI study schedule optimizer. Generate an optimal study schedule based on the following preferences and modules:
    
    User Preferences:
    - Date Range: {schedule_request["start_date"]} to {schedule_request["end_date"]}
    - Preferred Study Times: {', '.join(schedule_request["preferred_times"])}
    - Available Days: {', '.join(schedule_request["available_days"])}
    - Session Duration: {schedule_request["session_duration"]} minutes
    - Break Duration: {schedule_request["break_duration"]} minutes
    - Maximum Sessions Per Day: {schedule_request["max_sessions_per_day"]}
    
    Modules:
    {json.dumps([{"id": m["id"], "name": m["name"], "credits": m.get("credits", 0)} for m in modules], indent=2)}
    
    Follow these guidelines to create the optimal schedule:
    1. Allocate more time to modules with higher credits
    2. Distribute study sessions evenly across the available days
    3. Respect the preferred study times
    4. Respect the maximum sessions per day limit
    5. Don't schedule sessions on unavailable days
    6. Ensure adequate breaks between sessions
    7. Group related topics when possible
    
    Generate the schedule as a JSON array of study sessions with these fields:
    - date (ISO format date)
    - module (module id)
    - startTime (HH:MM format)
    - endTime (HH:MM format)
    - title (descriptive title including module name)
    - description (brief description of the study purpose)
    
    Return ONLY the valid JSON array without any surrounding text.
    """
    
    try:
        # Call the OpenAI API with updated client syntax
        if client:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI study scheduler that creates optimal study schedules based on user preferences and module information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            try:
                study_sessions = json.loads(ai_response)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract JSON content between code markers
                import re
                json_match = re.search(r'```json\n(.*?\n)```', ai_response, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                    study_sessions = json.loads(json_content)
                else:
                    # Fallback to manual scheduling
                    study_sessions = generate_fallback_schedule(schedule_request, modules)
        else:
            # No API key, use fallback scheduling
            study_sessions = generate_fallback_schedule(schedule_request, modules)
        
        # Convert AI response to actual schedule and sessions
        schedule = {
            "name": schedule_request.get("name", "AI Generated Study Schedule"),
            "start_date": schedule_request.get("start_date"),
            "end_date": schedule_request.get("end_date"),
            "preferred_times": schedule_request.get("preferred_times", []),
            "available_days": schedule_request.get("available_days", []),
            "session_duration": schedule_request.get("session_duration", 60),
            "break_duration": schedule_request.get("break_duration", 15),
            "max_sessions_per_day": schedule_request.get("max_sessions_per_day", 3),
            "modules": [m.get("id") for m in modules],
            "is_ai_generated": True
        }
        
        # Process the sessions
        processed_sessions = []
        for session in study_sessions:
            session_id = f"session_{str(uuid.uuid4())}"
            
            # Ensure required fields are present
            if not all(k in session for k in ["date", "module", "startTime", "endTime", "title"]):
                continue
            
            processed_session = {
                "id": session_id,
                "user_email": user_email,
                "type": "study_session",
                "title": session["title"],
                "module": session["module"],
                "date": session["date"],
                "startTime": session["startTime"],
                "endTime": session["endTime"],
                "description": session.get("description", "AI-generated study session"),
                "status": "planned",
                "completed": False
            }
            
            processed_sessions.append(processed_session)
        
        return schedule, processed_sessions
    
    except Exception as e:
        print(f"Error generating AI schedule: {str(e)}")
        return generate_fallback_schedule(schedule_request, modules)

def generate_fallback_schedule(schedule_request: dict, modules: List[dict]) -> tuple:
    """Generate a basic schedule without AI as a fallback"""
    # Create basic schedule object
    schedule = {
        "name": schedule_request.get("name", "Study Schedule"),
        "start_date": schedule_request.get("start_date"),
        "end_date": schedule_request.get("end_date"),
        "preferred_times": schedule_request.get("preferred_times", []),
        "available_days": schedule_request.get("available_days", []),
        "session_duration": schedule_request.get("session_duration", 60),
        "break_duration": schedule_request.get("break_duration", 15),
        "max_sessions_per_day": schedule_request.get("max_sessions_per_day", 3),
        "modules": [m.get("id") for m in modules],
        "is_ai_generated": False  # Not really AI-generated in this case
    }
    
    # Generate sessions using a simple algorithm
    sessions = []
    
    # Parse date range
    start_date = datetime.datetime.fromisoformat(schedule_request["start_date"].replace('Z', '+00:00')).date()
    end_date = datetime.datetime.fromisoformat(schedule_request["end_date"].replace('Z', '+00:00')).date()
    
    # Map day names to weekday indices
    day_mapping = {
        "monday": 0, "tuesday": 1, "wednesday": 2, 
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }
    
    # Convert available days to weekday indices
    available_days = schedule_request.get("available_days", [])
    available_day_indices = [day_mapping[day.lower()] for day in available_days if day.lower() in day_mapping]
    
    # Time slot mappings
    time_slots = {
        "morning": {"start": "09:00", "end": "10:00"},
        "afternoon": {"start": "14:00", "end": "15:00"},
        "evening": {"start": "18:00", "end": "19:00"},
        "night": {"start": "20:00", "end": "21:00"}
    }
    
    # Use preferred times or default to all times
    preferred_times = schedule_request.get("preferred_times", ["morning", "afternoon", "evening"])
    if not preferred_times:
        preferred_times = ["morning", "afternoon", "evening"]
    
    # Generate sessions for each day in the range
    current_date = start_date
    module_index = 0
    
    while current_date <= end_date:
        # Only schedule on available days
        if current_date.weekday() in available_day_indices:
            # Determine how many sessions to create for this day
            sessions_for_day = min(len(modules), schedule_request.get("max_sessions_per_day", 3))
            
            for i in range(sessions_for_day):
                # Select a module (round-robin)
                module = modules[module_index % len(modules)]
                module_index += 1
                
                # Select a time slot
                time_preference = preferred_times[i % len(preferred_times)]
                time_slot = time_slots.get(time_preference, time_slots["morning"])
                
                # Calculate end time based on session duration
                start_time = time_slot["start"]
                start_dt = datetime.datetime.strptime(start_time, "%H:%M")
                end_dt = start_dt + datetime.timedelta(minutes=schedule_request.get("session_duration", 60))
                end_time = end_dt.strftime("%H:%M")
                
                # Create session
                session_id = f"session_{str(uuid.uuid4())}"
                session = {
                    "id": session_id,
                    "title": f"{module.get('name')} Study Session",
                    "module": module.get("id"),
                    "date": current_date.isoformat(),
                    "startTime": start_time,
                    "endTime": end_time,
                    "description": f"Study session for {module.get('name')}",
                    "status": "planned",
                    "completed": False
                }
                
                sessions.append(session)
        
        # Move to next day
        current_date += datetime.timedelta(days=1)
    
    return schedule, sessions

def calculate_module_difficulty(module: dict) -> int:
    """Calculate the difficulty level of a module"""
    # In a real app, this could be based on user performance, credits, etc.
    # For now, use a simple heuristic based on credits
    credits = module.get("credits", 0)
    
    if credits >= 30:
        return 5  # Very difficult
    elif credits >= 20:
        return 4  # Difficult
    elif credits >= 15:
        return 3  # Moderate
    elif credits >= 10:
        return 2  # Easy
    else:
        return 1  # Very easy

def generate_ai_tips(user_email: str, sessions: List[dict], modules: List[dict], stats: dict, productivity_data: dict) -> List[dict]:
    """Generate personalized AI tips based on user's study data"""
    # Only generate tips if there are enough sessions to analyze
    if len(sessions) < 5:
        return []
    
    completed_sessions = [s for s in sessions if s.get("completed", False)]
    if len(completed_sessions) < 3:
        return []
    
    # Prepare context for AI
    context = {
        "completed_sessions": len(completed_sessions),
        "total_sessions": len(sessions),
        "completion_rate": stats.get("completion_rate", 0),
        "avg_productivity": stats.get("avg_productivity_rating", 0),
        "study_hours": stats.get("total_study_hours", 0),
        "productivity_by_time": productivity_data
    }
    
    # Create prompt for the AI
    prompt = f"""
    You are an AI study advisor. Generate personalized study tips based on the user's study data:
    
    Study Statistics:
    - Completed Sessions: {context["completed_sessions"]} out of {context["total_sessions"]}
    - Completion Rate: {context["completion_rate"]}%
    - Average Productivity Rating: {context["avg_productivity"]} out of 5
    - Total Study Hours: {context["study_hours"]} hours
    
    Productivity by Time of Day:
    {json.dumps(context["productivity_by_time"], indent=2)}
    
    Generate 2 personalized study tips that would help this user improve their study habits, 
    based on patterns in their data. Format each tip as a JSON object with these fields:
    - title (brief title for the tip)
    - text (detailed explanation of the tip, maximum 100 words)
    
    Return ONLY a JSON array of tip objects, without any surrounding text.
    """
    
    try:
        # Call the OpenAI API with updated client syntax
        if client:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI study advisor that provides personalized tips based on user study data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            try:
                tips_data = json.loads(ai_response)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract JSON content between code markers
                import re
                json_match = re.search(r'```json\n(.*?\n)```', ai_response, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                    tips_data = json.loads(json_content)
                else:
                    # Fallback to default tips
                    tips_data = generate_default_tips()
        else:
            # No API key, use default tips
            tips_data = generate_default_tips()
        
        # Process the tips
        processed_tips = []
        for tip in tips_data:
            tip_id = f"tip_{str(uuid.uuid4())}"
            
            processed_tip = {
                "id": tip_id,
                "title": tip.get("title", "Study Tip"),
                "text": tip.get("text", "Improve your study habits with regular practice."),
                "applied": False,
                "rejected": False
            }
            
            processed_tips.append(processed_tip)
        
        return processed_tips
    
    except Exception as e:
        print(f"Error generating AI tips: {str(e)}")
        return generate_default_tips()

def generate_default_tips() -> List[dict]:
    """Generate default tips if AI generation fails"""
    default_tips = [
        {
            "id": f"tip_{str(uuid.uuid4())}",
            "title": "Optimize Your Morning Sessions",
            "text": "Consider scheduling your most challenging subjects in the morning when your mind is fresh. Studies show cognitive performance is typically higher in the morning for most people.",
            "applied": False,
            "rejected": False
        },
        {
            "id": f"tip_{str(uuid.uuid4())}",
            "title": "Add More Breaks",
            "text": "Try the Pomodoro Technique: study for 25 minutes, then take a 5-minute break. This can help maintain concentration and prevent burnout during longer study sessions.",
            "applied": False,
            "rejected": False
        }
    ]
    
    return default_tips