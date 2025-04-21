# ai_scheduler.py
import os
import json
import datetime
import uuid
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from openai import AzureOpenAI  # Azure OpenAI client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Azure OpenAI client
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
client = None

if api_key and azure_endpoint:
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2023-05-15",
        azure_endpoint=azure_endpoint
    )

def call_openai_with_retry(prompt: str, max_retries: int = 3) -> Any:
    """Call OpenAI with retry logic for transient errors."""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": "You are an advanced AI study scheduler that creates personalized, optimized study schedules based on user preferences, module characteristics, and learning science principles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response
        except Exception as e:
            error_msg = str(e).lower()
            if ("rate limit" in error_msg or "timeout" in error_msg) and attempt < max_retries - 1:
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.warning(f"API rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"OpenAI API error: {str(e)}")
                raise

def get_user_productivity_patterns(user_email: str) -> Dict:
    """Get user's productivity patterns by time of day and day of week."""
    try:
        from study_database import get_productivity_patterns, get_completion_analytics
        
        # Get basic productivity patterns by time of day
        time_patterns = get_productivity_patterns(user_email)
        
        # Get more detailed completion analytics
        completion_data = get_completion_analytics(user_email)
        
        # Combine the data
        productivity_data = {
            "by_time_of_day": time_patterns.get("datasets", [{}])[0].get("data", []),
            "by_day_of_week": {
                day: data.get("rate", 0) 
                for day, data in completion_data.get("completion_by_day", {}).items()
            },
            "most_productive_module_times": {
                mod.get("name", ""): mod.get("avg_productivity", 0)
                for mod in completion_data.get("completion_by_module", {}).values()
            }
        }
        
        return productivity_data
    except Exception as e:
        logger.error(f"Error getting productivity patterns: {str(e)}")
        # Return default patterns
        return {
            "by_time_of_day": [],
            "by_day_of_week": {},
            "most_productive_module_times": {}
        }

def get_module_topic_suggestions(module_name: str, session_number: int) -> List[str]:
    """Generate specific topics for a study session based on module progression."""
    
    # Define module topic progressions for common subjects
    topic_progressions = {
        "Programming": [
            "Variables and Data Types", 
            "Control Structures",
            "Functions and Methods",
            "Object-Oriented Programming",
            "Error Handling and Debugging",
            "Data Structures",
            "Algorithms",
            "File I/O and Processing"
        ],
        "Mathematics": [
            "Number Systems",
            "Algebra and Functions",
            "Calculus Concepts",
            "Differential Equations",
            "Linear Algebra",
            "Probability Theory",
            "Statistics Applications",
            "Mathematical Modeling"
        ],
        "Computer Science": [
            "Computing Fundamentals",
            "Data Representation",
            "Boolean Logic",
            "Computer Architecture",
            "Operating Systems",
            "Networking Basics",
            "Database Concepts",
            "Software Engineering Principles"
        ],
        "Physics": [
            "Mechanics",
            "Thermodynamics",
            "Waves and Optics",
            "Electricity and Magnetism",
            "Modern Physics",
            "Quantum Mechanics",
            "Relativity",
            "Applied Physics"
        ],
        "Chemistry": [
            "Atomic Structure",
            "Periodic Table and Trends",
            "Chemical Bonding",
            "Reactions and Stoichiometry",
            "Thermochemistry",
            "Kinetics and Equilibrium",
            "Acids and Bases",
            "Organic Chemistry Basics"
        ]
    }
    
    # Match module name approximately to one of the categories
    matched_topics = []
    for category, topics in topic_progressions.items():
        if category.lower() in module_name.lower():
            # Get appropriate topics based on session number
            start_idx = min(session_number - 1, 0)
            end_idx = min(start_idx + 2, len(topics))
            matched_topics.extend(topics[start_idx:end_idx])
    
    # If no specific match, use generic study topics
    if not matched_topics:
        matched_topics = ["Key Concepts", "Important Theories", "Practical Applications"]
    
    return matched_topics[:3]  # Return up to 3 topics

def generate_study_schedule(user_email: str, schedule_request: dict, modules: List[dict]) -> Tuple[dict, List[dict]]:
    """Generate an optimized study schedule using AI with enhanced capabilities."""
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
    
    # Get user's productivity patterns
    productivity_data = get_user_productivity_patterns(user_email)
    context["productivity_data"] = productivity_data
    
    # Create more advanced prompt for AI
    prompt = f"""
    You are an advanced AI study scheduler creating a personalized, science-based study plan.

    USER PREFERENCES:
    - Date Range: {schedule_request["start_date"]} to {schedule_request["end_date"]}
    - Preferred Study Times: {', '.join(schedule_request["preferred_times"])}
    - Available Days: {', '.join(schedule_request["available_days"])}
    - Session Duration: {schedule_request["session_duration"]} minutes
    - Break Duration: {schedule_request["break_duration"]} minutes
    - Maximum Sessions Per Day: {schedule_request["max_sessions_per_day"]}

    MODULES:
    {json.dumps([{
        "id": m.get("id"),
        "name": m.get("name"),
        "code": m.get("code", ""),
        "credits": m.get("credits", 0),
        "difficulty": calculate_module_difficulty(m)
    } for m in modules], indent=2)}

    USER'S PRODUCTIVITY PATTERNS:
    {json.dumps(productivity_data, indent=2)}

    ADVANCED SCHEDULING GUIDELINES:
    1. Apply spaced repetition principles - study the same module every 2-3 days for optimal retention
    2. Place higher-difficulty modules during the user's most productive times of day
    3. Distribute modules evenly throughout the week to avoid cognitive overload
    4. Allocate more sessions to modules with higher credits or difficulty
    5. Schedule related modules on the same day to build connections between topics
    6. Avoid scheduling difficult modules back-to-back
    7. Create a progressive learning path that builds complexity over time
    8. Include brief review sessions of previously studied material
    9. Follow a learning science approach with interleaving different topics

    EACH SESSION MUST INCLUDE:
    - Specific topics to study (not just generic "Study Session")
    - A clear learning objective for the session
    - Appropriate placement based on the module's difficulty and user's productivity patterns
    
    EXAMPLE SESSION FORMAT:
    ```
    {
      "date": "2023-10-15",
      "module": "module_123",
      "startTime": "14:30",
      "endTime": "15:30",
      "title": "Data Structures: Trees & Graph Fundamentals",
      "description": "Focus on binary search trees, traversal algorithms, and basic graph representations.",
      "topics": ["Binary Search Trees", "Graph Representations", "Traversal Algorithms"]
    }
    ```

    Return ONLY a valid JSON array with exactly these fields for each session. 
    Do not include any explanation or additional text.
    """

    try:
        # Call the Azure OpenAI API with retry logic
        if client:
            response = call_openai_with_retry(prompt)
            ai_response = response.choices[0].message.content.strip()

            # Extract JSON from response
            try:
                study_sessions = json.loads(ai_response)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract JSON content between code markers
                import re
                json_match = re.search(r'```(?:json)?\n(.*?\n)```', ai_response, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                    study_sessions = json.loads(json_content)
                else:
                    # Fallback to manual scheduling
                    logger.warning("Failed to parse AI response as JSON. Using fallback scheduler.")
                    return generate_enhanced_fallback_schedule(user_email, schedule_request, modules)
        else:
            # No API key, use fallback scheduling
            logger.warning("OpenAI client not configured. Using fallback scheduler.")
            return generate_enhanced_fallback_schedule(user_email, schedule_request, modules)

        # Generate explanations for the schedule
        explanations = explain_schedule_decisions(study_sessions, modules)
        
        # Create actual schedule and sessions
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
            "is_ai_generated": True,
            "ai_explanations": explanations
        }

        # Process the sessions
        processed_sessions = []
        for session in study_sessions:
            session_id = f"session_{str(uuid.uuid4())}"

            # Ensure required fields are present
            if not all(k in session for k in ["date", "module", "startTime", "endTime", "title"]):
                continue

            # Make sure topics field is always a list
            if "topics" not in session or not isinstance(session["topics"], list):
                module_name = next((m["name"] for m in modules if m["id"] == session["module"]), "Unknown")
                session_idx = len([s for s in processed_sessions if s["module"] == session["module"]]) + 1
                session["topics"] = get_module_topic_suggestions(module_name, session_idx)

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
                "topics": session.get("topics", []),
                "status": "planned",
                "completed": False,
                "schedule_id": None  # Will be set after schedule is created
            }

            processed_sessions.append(processed_session)

        return schedule, processed_sessions

    except Exception as e:
        logger.error(f"Error generating AI schedule: {str(e)}")
        return generate_enhanced_fallback_schedule(user_email, schedule_request, modules)

def generate_enhanced_fallback_schedule(user_email: str, schedule_request: dict, modules: List[dict]) -> Tuple[dict, List[dict]]:
    """Generate an enhanced fallback schedule using data-driven approaches when AI fails."""
    # Get completion analytics if available
    try:
        from study_database import get_completion_analytics
        completion_data = get_completion_analytics(user_email)
        
        # Find most productive days and times
        best_days = [day for day, data in completion_data.get("completion_by_day", {}).items() 
                   if data.get("rate", 0) > 70]
        best_times = [time for time, data in completion_data.get("completion_by_time", {}).items() 
                    if data.get("rate", 0) > 70]
    except Exception:
        # Default values if analytics not available
        best_days = []
        best_times = []
    
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
        "is_ai_generated": True,  # Still mark as AI-generated for UI consistency
        "ai_explanations": [{
            "note": "This schedule was generated using a data-driven approach as a fallback."
        }]
    }

    # Generate sessions using a more sophisticated algorithm
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
    available_day_indices = [day_mapping.get(day.lower(), -1) for day in available_days]
    available_day_indices = [idx for idx in available_day_indices if idx >= 0]
    
    if not available_day_indices:
        # Default to weekdays if no valid days provided
        available_day_indices = [0, 1, 2, 3, 4]

    # Sort modules by difficulty/credits for better allocation
    modules_sorted = sorted(modules, 
                           key=lambda m: (calculate_module_difficulty(m), m.get("credits", 0)), 
                           reverse=True)

    # Time slot mappings with more variation
    time_slots = {
        "morning": [
            {"start": "08:00", "end": "09:00"},
            {"start": "09:30", "end": "10:30"},
            {"start": "11:00", "end": "12:00"}
        ],
        "afternoon": [
            {"start": "13:00", "end": "14:00"},
            {"start": "14:30", "end": "15:30"},
            {"start": "16:00", "end": "17:00"}
        ],
        "evening": [
            {"start": "17:30", "end": "18:30"},
            {"start": "19:00", "end": "20:00"}
        ],
        "night": [
            {"start": "20:30", "end": "21:30"}
        ]
    }

    # Use preferred times or default to all times
    preferred_times = schedule_request.get("preferred_times", ["morning", "afternoon", "evening"])
    if not preferred_times:
        preferred_times = ["morning", "afternoon", "evening"]

    # Track module study frequency for spaced repetition
    module_last_studied = {m.get("id"): None for m in modules}
    
    # Track sessions per day
    sessions_by_date = {}

    # Generate sessions for each day in the range
    current_date = start_date
    module_index = 0

    while current_date <= end_date:
        date_str = current_date.isoformat()
        
        # Only schedule on available days
        if current_date.weekday() in available_day_indices:
            # Initialize tracking for this date
            if date_str not in sessions_by_date:
                sessions_by_date[date_str] = 0
                
            # Determine modules to study today
            # First prioritize modules not studied recently
            today_modules = []
            
            # Sort modules by days since last study
            modules_by_priority = []
            for module in modules_sorted:
                module_id = module.get("id")
                days_since_last = float('inf')
                
                if module_last_studied[module_id]:
                    last_date = datetime.datetime.fromisoformat(module_last_studied[module_id]).date()
                    days_since_last = (current_date - last_date).days
                
                # Give higher priority to modules not studied in 2-3 days
                priority = 1
                if days_since_last >= 2:
                    priority = 10
                elif days_since_last == float('inf'):  # Never studied
                    priority = 5
                
                modules_by_priority.append((module, priority))
            
            # Sort by priority (higher first) and then by difficulty
            modules_by_priority.sort(key=lambda x: (x[1], calculate_module_difficulty(x[0])), reverse=True)
            
            # Select modules for today up to max_sessions_per_day
            max_sessions = min(len(modules), schedule_request.get("max_sessions_per_day", 3))
            today_modules = [m[0] for m in modules_by_priority[:max_sessions]]
            
            # Create sessions for selected modules
            for i, module in enumerate(today_modules):
                if sessions_by_date[date_str] >= max_sessions:
                    break
                
                # Get module ID and update last studied date
                module_id = module.get("id")
                module_last_studied[module_id] = date_str
                
                # Select time slot based on module difficulty
                # More difficult modules get morning slots if available
                difficulty = calculate_module_difficulty(module)
                preferred_time = preferred_times[i % len(preferred_times)]
                
                # For high difficulty modules, prefer morning if available
                if difficulty >= 4 and "morning" in preferred_times:
                    preferred_time = "morning"
                
                # Get available time slots
                time_options = time_slots.get(preferred_time, time_slots["afternoon"])
                time_slot = time_options[sessions_by_date[date_str] % len(time_options)]
                
                # Calculate end time based on session duration
                start_time = time_slot["start"]
                session_minutes = schedule_request.get("session_duration", 60)
                
                start_dt = datetime.datetime.strptime(start_time, "%H:%M")
                end_dt = start_dt + datetime.timedelta(minutes=session_minutes)
                end_time = end_dt.strftime("%H:%M")
                
                # Get module name
                module_name = module.get("name", "Module")
                
                # Generate study topics
                session_count = sum(1 for s in sessions if s.get("module") == module_id)
                topics = get_module_topic_suggestions(module_name, session_count + 1)
                
                # Create a more detailed title
                title = f"{module_name}: {topics[0]}" if topics else f"{module_name} Study Session"
                
                # Create session
                session_id = f"session_{str(uuid.uuid4())}"
                session = {
                    "id": session_id,
                    "user_email": user_email,
                    "type": "study_session",
                    "title": title,
                    "module": module_id,
                    "date": date_str,
                    "startTime": start_time,
                    "endTime": end_time,
                    "description": f"Focus on: {', '.join(topics)}",
                    "topics": topics,
                    "status": "planned",
                    "completed": False
                }
                
                sessions.append(session)
                sessions_by_date[date_str] += 1

        # Move to next day
        current_date += datetime.timedelta(days=1)

    return schedule, sessions

def explain_schedule_decisions(sessions: List[dict], modules: List[dict]) -> List[dict]:
    """Generate human-readable explanations for scheduling decisions."""
    explanations = []
    
    # Create a module lookup
    module_lookup = {m.get("id"): m for m in modules}
    
    # Group by day
    by_day = {}
    for session in sessions:
        day = session.get("date")
        if not day:
            continue
            
        if day not in by_day:
            by_day[day] = []
        by_day[day].append(session)
    
    # Analyze and explain each day's arrangement
    for day, day_sessions in by_day.items():
        # Skip days with no sessions
        if not day_sessions:
            continue
            
        # Get module names and difficulty levels
        day_modules = []
        difficulty_sum = 0
        
        for session in day_sessions:
            module_id = session.get("module")
            if module_id in module_lookup:
                module = module_lookup[module_id]
                module_name = module.get("name", "Unknown module")
                difficulty = calculate_module_difficulty(module)
                day_modules.append({"name": module_name, "difficulty": difficulty})
                difficulty_sum += difficulty
        
        # Skip if no valid modules found
        if not day_modules:
            continue
            
        # Calculate the average difficulty
        avg_difficulty = difficulty_sum / len(day_modules)
        
        # Generate day explanation
        day_explanation = {
            "day": day,
            "session_count": len(day_sessions),
            "modules": [m["name"] for m in day_modules],
            "avg_difficulty": round(avg_difficulty, 1),
            "reasoning": "This day's schedule "
        }
        
        # Add specific reasoning based on pattern
        if avg_difficulty > 3.5:
            day_explanation["reasoning"] += "focuses on more challenging modules that require high concentration. "
        elif len(day_modules) >= 3:
            day_explanation["reasoning"] += "interleaves multiple modules to enhance learning through varied practice. "
        else:
            day_explanation["reasoning"] += "provides focused study time for specific topics. "
            
        # Add time of day explanation
        morning_sessions = [s for s in day_sessions if s.get("startTime", "").startswith(("08", "09", "10", "11"))]
        if morning_sessions and avg_difficulty > 3:
            day_explanation["reasoning"] += "Challenging topics are scheduled in the morning for optimal focus."
        
        explanations.append(day_explanation)
    
    # Add overall schedule explanation
    if by_day:
        overall = {
            "type": "overall",
            "principle": "This schedule follows learning science principles including spaced repetition, "
                        "interleaving of topics, and difficulty-based time allocation."
        }
        explanations.append(overall)
    
    return explanations

def calculate_module_difficulty(module: dict) -> int:
    """Calculate the difficulty level of a module on a scale of 1-5."""
    # In a real app, this could be based on user performance, credits, etc.
    # Here we use a more sophisticated approach with multiple factors
    
    # Base difficulty on credits
    credits = module.get("credits", 0)
    difficulty = 1  # Default
    
    if credits >= 30:
        difficulty = 5  # Very difficult
    elif credits >= 20:
        difficulty = 4  # Difficult
    elif credits >= 15:
        difficulty = 3  # Moderate
    elif credits >= 10:
        difficulty = 2  # Easy
        
    # Adjust for module name keywords
    module_name = module.get("name", "").lower()
    difficulty_keywords = {
        "advanced": 1,
        "complex": 1,
        "higher": 0.5,
        "introduction": -0.5,
        "basic": -0.5,
        "fundamentals": -0.5
    }
    
    for keyword, adjustment in difficulty_keywords.items():
        if keyword in module_name:
            difficulty += adjustment
    
    # Ensure difficulty stays in range 1-5
    difficulty = max(1, min(5, difficulty))
    
    return difficulty

def generate_ai_tips(user_email: str, sessions: List[dict], modules: List[dict], stats: dict, productivity_data: dict) -> List[dict]:
    """Generate personalized AI tips based on user's study data."""
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
    
    # Add pattern analysis
    missed_sessions = [s for s in sessions if s.get("missed", False) or s.get("status") == "missed"]
    missed_times = {}
    for session in missed_sessions:
        start_time = session.get("startTime", "")
        hour = start_time.split(":")[0] if ":" in start_time else ""
        if hour:
            if hour not in missed_times:
                missed_times[hour] = 0
            missed_times[hour] += 1
    
    context["missed_session_patterns"] = missed_times
    
    # Add module completion patterns
    module_completion = {}
    for session in sessions:
        module_id = session.get("module")
        if module_id:
            if module_id not in module_completion:
                module_completion[module_id] = {"total": 0, "completed": 0}
            module_completion[module_id]["total"] += 1
            if session.get("completed", False):
                module_completion[module_id]["completed"] += 1
    
    context["module_completion"] = {
        module_id: {
            "completion_rate": (data["completed"] / data["total"] * 100) if data["total"] > 0 else 0,
            "module_name": next((m.get("name", "Unknown") for m in modules if m.get("id") == module_id), "Unknown")
        }
        for module_id, data in module_completion.items()
    }

    # Create prompt for the AI
    prompt = f"""
    You are an AI study advisor providing personalized study tips based on a student's actual study patterns.

    STUDY STATISTICS:
    - Completed Sessions: {context["completed_sessions"]} out of {context["total_sessions"]}
    - Completion Rate: {context["completion_rate"]}%
    - Average Productivity Rating: {context["avg_productivity"]} out of 5
    - Total Study Hours: {context["study_hours"]} hours

    PRODUCTIVITY BY TIME OF DAY:
    {json.dumps(context["productivity_by_time"], indent=2)}

    MISSED SESSION PATTERNS:
    {json.dumps(context["missed_session_patterns"], indent=2)}

    MODULE COMPLETION RATES:
    {json.dumps(context["module_completion"], indent=2)}

    GUIDELINES FOR GENERATING TIPS:
    1. Provide 3 personalized study tips based on the patterns in this data
    2. Focus on actionable advice the student can implement immediately
    3. Address patterns of missed sessions or low productivity
    4. Consider subject-specific strategies for modules with low completion rates
    5. Suggest evidence-based learning techniques
    6. Include a motivational element in at least one tip

    For each tip, provide:
    - A clear, concise title (maximum 8 words)
    - A detailed explanation (maximum 100 words)
    - A specific, actionable suggestion

    Return ONLY a JSON array of tip objects with "title" and "text" fields, no other text.
    """

    try:
        # Call the Azure OpenAI API with updated client syntax
        if client:
            response = call_openai_with_retry(prompt)
            ai_response = response.choices[0].message.content.strip()

            # Extract JSON from response
            try:
                tips_data = json.loads(ai_response)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract JSON content between code markers
                import re
                json_match = re.search(r'```(?:json)?\n(.*?\n)```', ai_response, re.DOTALL)
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
        logger.error(f"Error generating AI tips: {str(e)}")
        return generate_default_tips()

def generate_default_tips() -> List[dict]:
    """Generate default tips if AI generation fails."""
    default_tips = [
        {
            "id": f"tip_{str(uuid.uuid4())}",
            "title": "Optimize Your Most Productive Hours",
            "text": "Schedule your most challenging subjects during your peak productivity hours. Research shows that aligning difficult tasks with your natural energy cycles can improve retention by up to 30%.",
            "applied": False,
            "rejected": False
        },
        {
            "id": f"tip_{str(uuid.uuid4())}",
            "title": "Use the Pomodoro Technique",
            "text": "Try the Pomodoro Technique: 25 minutes of focused study followed by a 5-minute break. This structured approach can help maintain concentration and prevent burnout during longer study sessions.",
            "applied": False,
            "rejected": False
        },
        {
            "id": f"tip_{str(uuid.uuid4())}",
            "title": "Active Recall Beats Re-reading",
            "text": "Instead of passively re-reading notes, spend 10 minutes at the end of each study session testing yourself on what you've learned. Research shows active recall is 2x more effective than re-reading for long-term retention.",
            "applied": False,
            "rejected": False
        }
    ]

    return default_tips

def record_schedule_feedback(user_email: str, schedule_id: str, feedback_type: str, feedback_data: dict) -> bool:
    """Record user feedback on AI-generated schedules to improve future recommendations."""
    try:
        feedback_doc = {
            "id": f"schedule_feedback_{uuid.uuid4()}",
            "user_email": user_email,
            "schedule_id": schedule_id,
            "feedback_type": feedback_type,  # "rating", "modification", "completion"
            "feedback_data": feedback_data,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        # Store in database
        from database import _container
        _container.create_item(body=feedback_doc)
        return True
    except Exception as e:
        logger.error(f"Error recording schedule feedback: {str(e)}")
        return False

def learn_from_user_modifications(original_schedule: dict, modified_schedule: dict, original_sessions: List[dict], modified_sessions: List[dict]) -> dict:
    """Learn from how users modify AI-generated schedules."""
    try:
        modifications = {
            "schedule_changes": {},
            "session_changes": {},
            "time_preferences": {},
            "day_preferences": {}
        }
        
        # Track schedule-level changes
        for key in ["name", "preferred_times", "available_days", "session_duration", "max_sessions_per_day"]:
            if key in original_schedule and key in modified_schedule:
                if original_schedule[key] != modified_schedule[key]:
                    modifications["schedule_changes"][key] = {
                        "from": original_schedule[key],
                        "to": modified_schedule[key]
                    }
        
        # Find session-level modifications
        orig_sessions_map = {s["id"]: s for s in original_sessions}
        
        for mod_session in modified_sessions:
            session_id = mod_session.get("id")
            if session_id in orig_sessions_map:
                orig_session = orig_sessions_map[session_id]
                session_mods = {}
                
                # Check for time changes
                if orig_session.get("startTime") != mod_session.get("startTime"):
                    session_mods["startTime"] = {
                        "from": orig_session.get("startTime"),
                        "to": mod_session.get("startTime")
                    }
                    
                    # Track preferred time patterns
                    time_hour = int(mod_session.get("startTime", "00:00").split(":")[0])
                    module_id = mod_session.get("module")
                    
                    if module_id:
                        if module_id not in modifications["time_preferences"]:
                            modifications["time_preferences"][module_id] = {}
                        
                        # Group by time ranges
                        time_range = "morning" if 5 <= time_hour < 12 else \
                                    "afternoon" if 12 <= time_hour < 17 else \
                                    "evening" if 17 <= time_hour < 21 else "night"
                        
                        if time_range not in modifications["time_preferences"][module_id]:
                            modifications["time_preferences"][module_id][time_range] = 0
                        
                        modifications["time_preferences"][module_id][time_range] += 1
                
                # Check for date changes
                if orig_session.get("date") != mod_session.get("date"):
                    session_mods["date"] = {
                        "from": orig_session.get("date"),
                        "to": mod_session.get("date")
                    }
                    
                    # Track day of week preferences
                    try:
                        date_obj = datetime.datetime.fromisoformat(mod_session.get("date").replace('Z', '+00:00')).date()
                        day_index = date_obj.weekday()
                        day_name = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][day_index]
                        
                        module_id = mod_session.get("module")
                        if module_id:
                            if module_id not in modifications["day_preferences"]:
                                modifications["day_preferences"][module_id] = {}
                            
                            if day_name not in modifications["day_preferences"][module_id]:
                                modifications["day_preferences"][module_id][day_name] = 0
                            
                            modifications["day_preferences"][module_id][day_name] += 1
                    except Exception:
                        pass
                
                # Store session modifications if any were found
                if session_mods:
                    modifications["session_changes"][session_id] = session_mods
        
        # Record feedback for future learning
        record_schedule_feedback(
            user_email=original_schedule.get("user_email", "unknown"),
            schedule_id=original_schedule.get("id", "unknown"),
            feedback_type="modification",
            feedback_data=modifications
        )
        
        return modifications
    except Exception as e:
        logger.error(f"Error analyzing user modifications: {str(e)}")
        return {}