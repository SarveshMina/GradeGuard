# onboarding_routes.py
import azure.functions as func
import json
from datetime import datetime
from user_routes import verify_session
from database import get_user_by_email, _container

def get_onboarding_status(req: func.HttpRequest) -> func.HttpResponse:
    """Check if user has completed the onboarding questionnaire"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Check if onboarding completed
        has_completed = user_doc.get("hasCompletedOnboarding", False)
        
        # Check if calculator config exists
        has_calculator_config = "calculator" in user_doc and len(user_doc.get("calculator", {})) > 0
        
        # Check if has any modules
        query = f"SELECT COUNT(1) as count FROM c WHERE c.type = 'module' AND c.user_email = '{identity}'"
        results = list(_container.query_items(query=query, enable_cross_partition_query=True))
        has_modules = results[0]['count'] > 0 if results else False

        # Determine actual completion status - a user might have skipped the formal onboarding
        # but already set up their account
        is_effectively_onboarded = has_completed or (has_calculator_config and has_modules)
        
        # If effectively onboarded but flag not set, update the flag
        if is_effectively_onboarded and not has_completed:
            user_doc["hasCompletedOnboarding"] = True
            _container.upsert_item(user_doc)

        return func.HttpResponse(
            json.dumps({
                "hasCompletedOnboarding": is_effectively_onboarded,
                "hasCalculatorConfig": has_calculator_config,
                "hasModules": has_modules
            }),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def save_onboarding_questionnaire(req: func.HttpRequest) -> func.HttpResponse:
    """Save the onboarding questionnaire data"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get questionnaire data
        questionnaire_data = req.get_json()
        
        # Get user document
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
        
        # Save step 1 - Education details
        if "educationDetails" in questionnaire_data:
            education = questionnaire_data["educationDetails"]
            user_doc["educationLevel"] = education.get("level", "")  # Undergraduate, Postgraduate, etc.
            user_doc["studyMode"] = education.get("mode", "")  # Full-time, Part-time
            user_doc["studyTimes"] = education.get("studyTimes", [])  # Morning, Afternoon, Evening
        
        # Save step 2 - Degree structure
        if "degreeStructure" in questionnaire_data:
            degree = questionnaire_data["degreeStructure"]
            
            # Initialize calculator if not exists
            if "calculator" not in user_doc:
                user_doc["calculator"] = {}
            
            # Create years array based on total years
            total_years = degree.get("totalYears", 3)
            semesters_per_year = degree.get("semestersPerYear", 2)
            credits_per_year = degree.get("creditsPerYear", 120)
            
            # Build years configuration
            years = []
            for i in range(1, total_years + 1):
                current_year = f"Year {i}"
                is_current = degree.get("currentYear") == current_year
                
                years.append({
                    "year": current_year,
                    "active": True,
                    "credits": credits_per_year,
                    "weight": degree.get("yearWeights", {}).get(current_year, 0),
                    "semesters": semesters_per_year,
                    "isCurrent": is_current
                })
            
            user_doc["calculator"]["years"] = years
            user_doc["calculator"]["degreeType"] = degree.get("degreeType", "UK Percentage")
            user_doc["calculator"]["targetGrade"] = degree.get("targetGrade", 70)
        
        # Mark onboarding as completed
        user_doc["hasCompletedOnboarding"] = True
        user_doc["onboardingCompletedAt"] = datetime.utcnow().isoformat()
        
        # Save changes
        _container.upsert_item(user_doc)
        
        return func.HttpResponse(
            json.dumps({
                "message": "Onboarding questionnaire saved successfully",
                "hasCompletedOnboarding": True
            }),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)