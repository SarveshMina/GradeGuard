# grade_calculator.py
import json
from typing import List, Dict, Any, Optional
from database import get_user_by_email, _container

def get_user_modules(email: str) -> List[Dict[str, Any]]:
    """Retrieve modules for a user"""
    query = f"SELECT * FROM c WHERE c.type = 'module' AND c.user_email = '{email}'"
    modules = list(_container.query_items(query=query, enable_cross_partition_query=True))
    return modules

def get_modules_by_year_semester(email: str) -> Dict[str, Dict[int, List[Dict[str, Any]]]]:
    """Get modules organized by year and semester"""
    modules = get_user_modules(email)
    organized = {}
    
    for module in modules:
        year = module.get("year", "Unknown")
        semester = module.get("semester", 1)
        
        if year not in organized:
            organized[year] = {}
            
        if semester not in organized[year]:
            organized[year][semester] = []
            
        organized[year][semester].append(module)
    
    return organized

def calculate_year_average(modules: List[Dict[str, Any]], year: str) -> float:
    """Calculate the weighted average for a specific year"""
    year_modules = [m for m in modules if m.get("year") == year]

    if not year_modules:
        return 0.0

    total_credits = sum(m.get("credits", 0) for m in year_modules)
    if total_credits == 0:
        return 0.0

    weighted_sum = sum(m.get("score", 0) * m.get("credits", 0) for m in year_modules)
    return round(weighted_sum / total_credits, 1)

def calculate_semester_average(modules: List[Dict[str, Any]], year: str, semester: int) -> float:
    """Calculate the weighted average for a specific semester within a year"""
    semester_modules = [
        m for m in modules 
        if m.get("year") == year and m.get("semester") == semester
    ]

    if not semester_modules:
        return 0.0

    total_credits = sum(m.get("credits", 0) for m in semester_modules)
    if total_credits == 0:
        return 0.0

    weighted_sum = sum(m.get("score", 0) * m.get("credits", 0) for m in semester_modules)
    return round(weighted_sum / total_credits, 1)

def calculate_overall_average(modules: List[Dict[str, Any]], year_weights: Dict[str, float]) -> float:
    """Calculate overall weighted average based on year weights"""
    if not modules or not year_weights:
        return 0.0

    year_averages = {}
    for year in year_weights.keys():
        year_averages[year] = calculate_year_average(modules, year)

    total_weight = sum(weight for year, weight in year_weights.items() if year_averages.get(year, 0) > 0)
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(year_averages.get(year, 0) * weight for year, weight in year_weights.items())
    return round(weighted_sum / total_weight, 1)

def calculate_remaining_grade_needed(
    current_average: float,
    target_grade: float,
    completed_credits: int,
    total_credits: int
) -> float:
    """Calculate the average grade needed on remaining credits to achieve target"""
    if completed_credits >= total_credits:
        return 0.0

    remaining_credits = total_credits - completed_credits
    current_points = current_average * completed_credits
    target_points = target_grade * total_credits

    points_needed = target_points - current_points
    if points_needed <= 0:
        return 0.0

    return round(points_needed / remaining_credits, 1)

def get_dashboard_stats(email: str) -> Dict[str, Any]:
    """Generate dashboard statistics for a user"""
    user_doc = get_user_by_email(email)
    if not user_doc:
        return {"error": "User not found"}

    # Extract configuration
    calculator_config = user_doc.get("calculator", {})
    year_settings = {y.get("year"): y.get("weight", 0) for y in calculator_config.get("years", []) if y.get("active", False)}

    # Get modules
    modules = get_user_modules(email)
    
    # Calculate statistics
    stats = {
        "overallAverage": 0.0,
        "yearlyAverages": {},
        "semesterAverages": {},
        "completedCredits": 0,
        "totalCredits": 0,
        "topModule": {"name": "N/A", "score": 0},
        "yearData": [],
        "gradeDistribution": [],
        "modulesByYearSemester": {}
    }

    if not modules:
        return stats

    # Calculate completed credits
    stats["completedCredits"] = sum(m.get("credits", 0) for m in modules)

    # Calculate total credits from config
    stats["totalCredits"] = sum(y.get("credits", 0) for y in calculator_config.get("years", []) if y.get("active", False))

    # Find top module
    if modules:
        top_module = max(modules, key=lambda m: m.get("score", 0))
        stats["topModule"] = {
            "name": top_module.get("name", "Unknown"),
            "score": top_module.get("score", 0)
        }

    # Calculate year averages and organize modules by year and semester
    modules_by_year_semester = {}
    
    for year, weight in year_settings.items():
        year_avg = calculate_year_average(modules, year)
        stats["yearlyAverages"][year] = year_avg

        year_modules = [m for m in modules if m.get("year") == year]
        completed_credits = sum(m.get("credits", 0) for m in year_modules)
        year_config = next((y for y in calculator_config.get("years", []) if y.get("year") == year), None)
        total_credits = year_config.get("credits", 0) if year_config else 0

        # Calculate semester averages for this year
        semesters_in_year = {}
        semesters_data = []
        
        # Get distinct semesters in this year's modules
        semester_set = set(m.get("semester", 1) for m in year_modules)
        
        for semester in sorted(semester_set):
            semester_avg = calculate_semester_average(modules, year, semester)
            semester_key = f"{year}_sem{semester}"
            stats["semesterAverages"][semester_key] = semester_avg
            
            # Get modules for this semester
            semester_modules = [m for m in year_modules if m.get("semester", 1) == semester]
            semester_credits = sum(m.get("credits", 0) for m in semester_modules)
            
            semesters_data.append({
                "semester": semester,
                "average": semester_avg,
                "credits": semester_credits
            })
            
            # Organize modules for the frontend
            if year not in modules_by_year_semester:
                modules_by_year_semester[year] = {}
                
            modules_by_year_semester[year][semester] = semester_modules

        stats["yearData"].append({
            "name": year,
            "average": year_avg,
            "credits": completed_credits,
            "totalCredits": total_credits,
            "weight": weight,
            "semesters": semesters_data
        })

    # Add the organized modules to stats
    stats["modulesByYearSemester"] = modules_by_year_semester

    # Calculate overall average
    stats["overallAverage"] = calculate_overall_average(modules, year_settings)

    # Calculate grade distribution
    ranges = [
        {"name": "0-39%", "range": [0, 39], "count": 0},
        {"name": "40-49%", "range": [40, 49], "count": 0},
        {"name": "50-59%", "range": [50, 59], "count": 0},
        {"name": "60-69%", "range": [60, 69], "count": 0},
        {"name": "70-100%", "range": [70, 100], "count": 0}
    ]

    for m in modules:
        score = m.get("score", 0)
        for r in ranges:
            if r["range"][0] <= score <= r["range"][1]:
                r["count"] += 1
                break

    stats["gradeDistribution"] = ranges

    # Calculate target grades needed
    remaining_credits = stats["totalCredits"] - stats["completedCredits"]
    if remaining_credits > 0:
        stats["targetHighGrade"] = calculate_remaining_grade_needed(
            stats["overallAverage"], 70, stats["completedCredits"], stats["totalCredits"])
        stats["targetMediumGrade"] = calculate_remaining_grade_needed(
            stats["overallAverage"], 60, stats["completedCredits"], stats["totalCredits"])
        stats["targetLowGrade"] = calculate_remaining_grade_needed(
            stats["overallAverage"], 50, stats["completedCredits"], stats["totalCredits"])
    else:
        stats["targetHighGrade"] = 0
        stats["targetMediumGrade"] = 0
        stats["targetLowGrade"] = 0

    return stats

def get_prediction_analysis(email: str) -> Dict[str, Any]:
    """Generate prediction analysis for future performance"""
    modules = get_user_modules(email)
    
    if not modules:
        return {
            "bestCaseGrade": 0,
            "expectedGrade": 0,
            "worstCaseGrade": 0,
            "variability": 0
        }
        
    # Calculate average, best and worst scores
    scores = [m.get("score", 0) for m in modules]
    avg_score = sum(scores) / len(scores) if scores else 0
    best_score = max(scores) if scores else 0
    worst_score = min(scores) if scores else 0
    
    # Calculate variability (standard deviation)
    variance = sum((s - avg_score) ** 2 for s in scores) / len(scores) if scores else 0
    std_dev = variance ** 0.5
    
    # Calculate prediction metrics
    best_case = min(100, avg_score + (best_score - avg_score) * 0.5)
    expected = avg_score
    worst_case = max(0, avg_score - (avg_score - worst_score) * 0.5)
    
    return {
        "bestCaseGrade": round(best_case, 1),
        "expectedGrade": round(expected, 1),
        "worstCaseGrade": round(worst_case, 1),
        "variability": round(std_dev, 1)
    }

def calculate_completion_percentages(email: str) -> dict:
    """Calculate the achieved, lost, and remaining percentage breakdown"""
    user_doc = get_user_by_email(email)
    if not user_doc:
        return {"achieved": 0, "lost": 0, "remaining": 100}
    
    # Get calculator config
    calculator_config = user_doc.get("calculator", {})
    years_config = calculator_config.get("years", [])
    
    # Get all modules
    modules = get_user_modules(email)
    
    # Calculate total credits in degree
    total_credits = sum(year.get("credits", 0) for year in years_config if year.get("active", False))
    if total_credits == 0:
        return {"achieved": 0, "lost": 0, "remaining": 100}
    
    # Calculate credits obtained so far
    earned_credits = sum(module.get("credits", 0) for module in modules)
    
    # Calculate percentage achieved (credits earned / total credits)
    achieved_percentage = (earned_credits / total_credits) * 100
    
    # Get current average score
    average_score = 0
    if modules:
        total_weighted_score = sum(module.get("score", 0) * module.get("credits", 0) for module in modules)
        average_score = total_weighted_score / earned_credits if earned_credits > 0 else 0
    
    # Calculate maximum possible score (100%)
    max_possible_score = 100
    
    # Calculate lost percentage: what percentage points were lost due to not achieving perfect scores
    lost_percentage = (achieved_percentage * (max_possible_score - average_score)) / 100 if average_score > 0 else 0
    
    # Calculate remaining percentage: what percentage of the degree is still to be completed
    remaining_percentage = 100 - achieved_percentage
    
    return {
        "achieved": round(achieved_percentage, 1),
        "lost": round(lost_percentage, 1),
        "remaining": round(remaining_percentage, 1)
    }