# dashboard_routes.py
import azure.functions as func
import json
from user_routes import verify_session
from database import get_user_by_email, _container, get_user_modules
from grade_calculator import get_dashboard_stats, get_prediction_analysis
from datetime import datetime

def get_dashboard_data(req: func.HttpRequest) -> func.HttpResponse:
    """Get all dashboard data including grade statistics"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get statistics
        stats = get_dashboard_stats(identity)
        
        # Get predictions
        predictions = get_prediction_analysis(identity)
        stats["predictions"] = predictions

        # Get user dashboard configuration
        user_doc = get_user_by_email(identity)
        dashboard_config = user_doc.get("dashboardConfig", {})
        
        # Add personal information
        stats["userProfile"] = {
            "firstName": user_doc.get("firstName", ""),
            "lastName": user_doc.get("lastName", ""),
            "university": user_doc.get("university", ""),
            "degree": user_doc.get("degree", ""),
            "email": user_doc.get("email", ""),
            "avatar": user_doc.get("avatar", "")
        }

        # Combine data
        response_data = {
            "stats": stats,
            "config": dashboard_config
        }

        return func.HttpResponse(json.dumps(response_data), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def update_dashboard_config(req: func.HttpRequest) -> func.HttpResponse:
    """Update dashboard configuration preferences"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        config_data = req.get_json()
        user_doc = get_user_by_email(identity)

        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Update or create dashboard config
        if "dashboardConfig" not in user_doc:
            user_doc["dashboardConfig"] = {}

        # Update specific sections
        for key, value in config_data.items():
            user_doc["dashboardConfig"][key] = value

        # Save to database
        _container.upsert_item(user_doc)

        return func.HttpResponse(json.dumps(user_doc["dashboardConfig"]), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def add_activity(req: func.HttpRequest) -> func.HttpResponse:
    """Add a new activity to the recent activities list"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        activity_data = req.get_json()
        user_doc = get_user_by_email(identity)

        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Ensure required fields
        required_fields = ["title", "description", "type", "time"]
        for field in required_fields:
            if field not in activity_data:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400
                )

        # Initialize activities array if it doesn't exist
        if "dashboardConfig" not in user_doc:
            user_doc["dashboardConfig"] = {}
        if "recentActivities" not in user_doc["dashboardConfig"]:
            user_doc["dashboardConfig"]["recentActivities"] = []

        # Add timestamp if not provided
        if "timestamp" not in activity_data:
            activity_data["timestamp"] = datetime.utcnow().isoformat()

        # Add new activity to the beginning
        user_doc["dashboardConfig"]["recentActivities"].insert(0, activity_data)

        # Limit to 10 activities
        user_doc["dashboardConfig"]["recentActivities"] = user_doc["dashboardConfig"]["recentActivities"][:10]

        # Save to database
        _container.upsert_item(user_doc)

        return func.HttpResponse(
            json.dumps(user_doc["dashboardConfig"]["recentActivities"]),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def update_goals(req: func.HttpRequest) -> func.HttpResponse:
    """Update user goals"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        goals_data = req.get_json()
        user_doc = get_user_by_email(identity)

        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Initialize if needed
        if "dashboardConfig" not in user_doc:
            user_doc["dashboardConfig"] = {}

        # Update goals
        user_doc["dashboardConfig"]["goals"] = goals_data
        
        # Calculate goal progress based on current stats
        stats = get_dashboard_stats(identity)
        current_avg = stats.get("overallAverage", 0)
        
        for goal in user_doc["dashboardConfig"]["goals"]:
            if "target_score" in goal:
                target = goal.get("target_score", 100)
                # Calculate progress as percentage of target achieved
                if target > 0:
                    progress = min(100, (current_avg / target) * 100)
                    goal["progress"] = round(progress, 1)

        # Save to database
        _container.upsert_item(user_doc)

        return func.HttpResponse(json.dumps(user_doc["dashboardConfig"]["goals"]), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def get_insights(req: func.HttpRequest) -> func.HttpResponse:
    """Get insights based on user's academic data"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get user modules and statistics
        stats = get_dashboard_stats(identity)
        predictions = get_prediction_analysis(identity)
        
        # Generate insights
        insights = []
        
        # Insight based on overall average
        overall_avg = stats.get("overallAverage", 0)
        if overall_avg >= 70:
            insights.append({
                "type": "positive",
                "title": "Excellent Performance",
                "description": f"Your overall average of {overall_avg}% is in the First Class range. Keep up the great work!"
            })
        elif overall_avg >= 60:
            insights.append({
                "type": "positive",
                "title": "Strong Performance",
                "description": f"Your overall average of {overall_avg}% is in the 2:1 range. You're doing well!"
            })
        elif overall_avg >= 50:
            insights.append({
                "type": "neutral",
                "title": "Satisfactory Performance",
                "description": f"Your overall average of {overall_avg}% is in the 2:2 range. Consider focusing on improvement strategies."
            })
        elif overall_avg >= 40:
            insights.append({
                "type": "warning",
                "title": "Improvement Needed",
                "description": f"Your overall average of {overall_avg}% is in the Third Class range. Consider seeking academic support."
            })
        elif overall_avg > 0:
            insights.append({
                "type": "critical",
                "title": "Critical Performance Alert",
                "description": f"Your overall average of {overall_avg}% is below passing level. Please speak with your academic advisor immediately."
            })
            
        # Insight based on grade distribution
        grade_dist = stats.get("gradeDistribution", [])
        first_class_count = next((item["count"] for item in grade_dist if item["name"] == "70-100%"), 0)
        third_or_fail_count = sum(item["count"] for item in grade_dist if item["name"] in ["0-39%", "40-49%"])
        
        total_modules = sum(item["count"] for item in grade_dist)
        
        if total_modules > 0:
            first_class_percentage = (first_class_count / total_modules) * 100
            lower_grades_percentage = (third_or_fail_count / total_modules) * 100
            
            if first_class_percentage >= 50:
                insights.append({
                    "type": "positive",
                    "title": "Consistent Excellence",
                    "description": f"{round(first_class_percentage)}% of your modules are in the First Class range, showing consistent excellence."
                })
            elif lower_grades_percentage >= 30:
                insights.append({
                    "type": "warning",
                    "title": "Inconsistent Performance",
                    "description": f"{round(lower_grades_percentage)}% of your modules are below 2:2 level. Focus on bringing these up."
                })
        
        # Add prediction insights
        best_case = predictions.get("bestCaseGrade", 0)
        expected = predictions.get("expectedGrade", 0)
        worst_case = predictions.get("worstCaseGrade", 0)
        
        insights.append({
            "type": "prediction",
            "title": "Performance Prediction",
            "description": f"Based on your current performance, we predict your final grade to be around {expected}%, with a range of {worst_case}% to {best_case}%."
        })
        
        # Add recommendations
        target_high = stats.get("targetHighGrade", 0)
        if target_high > 0 and target_high <= 100:
            insights.append({
                "type": "recommendation",
                "title": "First Class Goal",
                "description": f"To achieve a First Class degree, you need to average {target_high}% in your remaining modules."
            })
            
        # Response with all insights
        response = {
            "insights": insights,
            "predictions": predictions,
            "strengths": get_strengths_and_weaknesses(identity)["strengths"],
            "weaknesses": get_strengths_and_weaknesses(identity)["weaknesses"]
        }
        
        return func.HttpResponse(json.dumps(response), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_strengths_and_weaknesses(user_email: str) -> dict:
    """Identify user's academic strengths and weaknesses based on module performance"""
    # Get all user modules
    modules = get_user_modules(user_email)
    
    if not modules or len(modules) < 2:
        return {
            "strengths": [],
            "weaknesses": []
        }
    
    # Calculate average score
    average_score = sum(m.get("score", 0) for m in modules) / len(modules)
    
    # Sort modules by score
    sorted_modules = sorted(modules, key=lambda m: m.get("score", 0), reverse=True)
    
    # Get top and bottom modules (strengths and weaknesses)
    num_to_show = min(3, len(modules) // 2)
    strengths = sorted_modules[:num_to_show]
    weaknesses = sorted_modules[-num_to_show:]
    
    # Format for output
    strength_data = [
        {
            "name": m.get("name", "Unknown"),
            "score": m.get("score", 0),
            "year": m.get("year", "Unknown"),
            "semester": m.get("semester", 1),
            "variance": round(m.get("score", 0) - average_score, 1)
        }
        for m in strengths
    ]
    
    weakness_data = [
        {
            "name": m.get("name", "Unknown"),
            "score": m.get("score", 0),
            "year": m.get("year", "Unknown"),
            "semester": m.get("semester", 1),
            "variance": round(m.get("score", 0) - average_score, 1)
        }
        for m in weaknesses
    ]
    
    return {
        "strengths": strength_data,
        "weaknesses": weakness_data
    }