# ai_service.py
import os
import json
import datetime
import logging
from typing import List, Dict, Any, Optional
import openai
from models import (
    StudyPreferences, 
    ModuleStudyPreference, 
    StudySession, 
    OpenAIScheduleRequest,
    ScheduleGenerationResponse
)

# Configure OpenAI API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_openai():
    """Initialize the OpenAI API connection"""
    try:
        # Create a client instance instead of setting api_key directly
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI API initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Error initializing OpenAI API: {str(e)}")
        return None

def format_calendar_events(events: List[Dict[str, Any]]) -> str:
    """Format calendar events into a readable string for the AI"""
    event_lines = []
    
    for event in events:
        start_time = event.get("start_time", event.get("date"))
        end_time = event.get("end_time", "")
        all_day = event.get("all_day", False)
        
        if all_day:
            time_str = f"All day on {start_time}"
        else:
            time_str = f"{start_time} to {end_time}"
            
        event_lines.append(f"Event: {event.get('title')} - {time_str} - Type: {event.get('type', 'general')}")
    
    return "\n".join(event_lines)

def generate_study_schedule(request: OpenAIScheduleRequest) -> ScheduleGenerationResponse:
    """Generate an optimized study schedule using OpenAI"""
    try:
        client = initialize_openai()
        if not client:
            raise Exception("Failed to initialize OpenAI API")
        
        # Prepare data for the prompt
        preferences = request.study_preferences
        module_prefs = request.module_preferences
        events = request.existing_events
        
        # Get module details
        module_details = []
        for mod_pref in module_prefs:
            assessments = ", with assessments on " + ", ".join(mod_pref.assessment_dates) if mod_pref.assessment_dates else ""
            topics = f", covering topics: {', '.join(mod_pref.topics)}" if mod_pref.topics else ""
            
            module_details.append(
                f"Module ID: {mod_pref.module_id}, Priority: {mod_pref.priority}/5, " +
                f"Weekly goal: {mod_pref.weekly_hours_goal} hours, Difficulty: {mod_pref.difficulty_rating}/5" +
                f"{assessments}{topics}"
            )
        
        # Format calendar events
        calendar_section = format_calendar_events(events)
        
        # Build the prompt
        prompt = f"""
        I need to create an optimized study schedule for a student with the following preferences:
        
        STUDY PREFERENCES:
        - Preferred times of day: {', '.join(preferences.preferred_times)}
        - Available days: {', '.join(preferences.available_days)}
        - Preferred session duration: {preferences.session_duration} minutes
        - Preferred break duration: {preferences.break_duration} minutes
        - Maximum sessions per day: {preferences.max_sessions_per_day}
        - Learning environment: {preferences.environment_preference}
        
        FOCUS LEVELS BY TIME:
        {json.dumps(preferences.focus_levels, indent=2)}
        
        SPECIFIC AVAILABLE TIME RANGES:
        {json.dumps(preferences.specific_time_ranges, indent=2) if preferences.specific_time_ranges else "No specific time constraints"}
        
        MODULES TO STUDY:
        {chr(10).join(module_details)}
        
        EXISTING CALENDAR COMMITMENTS:
        {calendar_section}
        
        SCHEDULING PERIOD:
        From {request.start_date} to {request.end_date}
        
        Please create an optimized study schedule that:
        1. Respects the student's preferences and availability
        2. Allocates more time to higher priority and more difficult modules
        3. Schedules study sessions for assessment preparation
        4. Avoids conflicts with existing calendar events
        5. Applies spaced repetition principles for better learning
        6. Schedules more challenging subjects during high-focus periods
        
        Return the schedule as a JSON array with the following structure for each study session:
        {{
          "module_id": string,
          "module_name": string,
          "start_time": ISO datetime string,
          "end_time": ISO datetime string,
          "topics": [strings] (optional),
          "location": string (optional)
        }}
        
        Also include a "recommendations" array with study tips specific to this schedule and modules.
        """
        
        # Call OpenAI API with updated client API
        response = client.chat.completions.create(
            model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are an AI assistant that creates optimized study schedules for students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=4000
        )
        
        # Extract the generated text (updated for new API)
        generated_text = response.choices[0].message.content
            
        # Parse the response
        # First, find the JSON part of the response
        import re
        json_match = re.search(r'```(?:json)?\s*(\[[\s\S]*?\]|\{[\s\S]*?\})\s*```', generated_text)
        
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON without code blocks
            json_match = re.search(r'(\[[\s\S]*?\]|\{[\s\S]*?\})', generated_text)
            if json_match:
                json_str = json_match.group(1)
            else:
                raise Exception("Could not parse JSON from AI response")
        
        # Parse JSON
        try:
            schedule_data = json.loads(json_str)
        except json.JSONDecodeError:
            # Try fixing common JSON issues
            fixed_json = json_str.replace("'", '"')
            schedule_data = json.loads(fixed_json)
            
        # Extract recommendations (if any)
        recommendations = []
        recommendations_match = re.search(r'"recommendations":\s*\[(.*?)\]', generated_text, re.DOTALL)
        if recommendations_match:
            recommendations_str = recommendations_match.group(1)
            # Extract strings between quotes
            import re
            recommendations = re.findall(r'"([^"]*)"', recommendations_str)
        
        # Check if we have a direct JSON object or a list of sessions
        if isinstance(schedule_data, dict):
            study_sessions = schedule_data.get("study_sessions", [])
            recommendations = schedule_data.get("recommendations", recommendations)
        else:
            study_sessions = schedule_data
            
        # Convert to StudySession objects
        sessions = []
        module_hours = {}
        total_hours = 0
        
        for session in study_sessions:
            # Get module name if it doesn't exist in the data
            if "module_name" not in session:
                for mod_pref in module_prefs:
                    if mod_pref.module_id == session["module_id"]:
                        session["module_name"] = mod_pref.module_id.split(":")[-1]  # Extract name from ID as fallback
                        break
            
            # Create StudySession object
            study_session = StudySession(
                user_email=request.user_email,
                status="planned",
                **session
            )
            sessions.append(study_session)
            
            # Calculate hours per module
            module_id = session["module_id"]
            start = datetime.datetime.fromisoformat(session["start_time"].replace('Z', '+00:00'))
            end = datetime.datetime.fromisoformat(session["end_time"].replace('Z', '+00:00'))
            duration_hours = (end - start).total_seconds() / 3600
            
            if module_id in module_hours:
                module_hours[module_id] += duration_hours
            else:
                module_hours[module_id] = duration_hours
                
            total_hours += duration_hours
        
        # Create response
        response = ScheduleGenerationResponse(
            study_sessions=sessions,
            total_study_hours=round(total_hours, 1),
            module_distribution=module_hours,
            recommendations=recommendations
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating study schedule: {str(e)}")
        logger.error(f"Traceback: {__import__('traceback').format_exc()}")
        raise Exception(f"Failed to generate study schedule: {str(e)}")


def suggest_study_topics(module_id: str, topics: List[str], assessment_date: Optional[str] = None) -> List[str]:
    """Suggest specific topics to focus on for a study session"""
    try:
        client = initialize_openai()
        if not client:
            raise Exception("Failed to initialize OpenAI API")
        
        assessment_context = ""
        if assessment_date:
            assessment_date_obj = datetime.datetime.fromisoformat(assessment_date.replace('Z', '+00:00'))
            today = datetime.datetime.now()
            days_until_assessment = (assessment_date_obj - today).days
            
            if days_until_assessment <= 7:
                assessment_context = f"There is an assessment in {days_until_assessment} days."
            elif days_until_assessment <= 14:
                assessment_context = f"There is an assessment in {days_until_assessment} days, so preparation should begin."
        
        prompt = f"""
        For a study session in module {module_id} covering these topics:
        {', '.join(topics)}
        
        {assessment_context}
        
        Please suggest 3-5 specific topics or concepts to focus on during this study session, 
        considering principles of spaced repetition and effectiveness of learning.
        
        Return only the list of topics, one per line.
        """
        
        # Call OpenAI API with updated client API
        response = client.chat.completions.create(
            model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful study advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        # Extract the generated text (updated for new API)
        generated_text = response.choices[0].message.content
        
        # Parse response into list of topics
        suggested_topics = [line.strip() for line in generated_text.strip().split('\n') if line.strip()]
        return suggested_topics[:5]  # Return max 5 topics
        
    except Exception as e:
        logger.error(f"Error suggesting study topics: {str(e)}")
        # Return a fallback response rather than failing
        return topics[:3] if topics else ["General review"]