# graderadar_routes.py
import azure.functions as func
import json
import uuid
import datetime
from typing import List, Dict, Any
from user_routes import verify_session
from models import ModuleReview
from database import (
    get_module_reviews, 
    create_module_review, 
    delete_module_review,
    get_module_statistics,
    get_university_modules_with_stats,
    get_degree_modules_with_stats,
    get_module_by_id_public
)

def get_universities_with_data(req: func.HttpRequest) -> func.HttpResponse:
    """Get list of universities that have modules with reviews"""
    try:
        from database import get_all_universities_docs
        university_docs = get_all_universities_docs()
        
        # Filter to include only universities with degrees that have modules
        universities_with_data = []
        
        for uni in university_docs:
            if "degrees" in uni and uni["degrees"]:
                # Check if any degree has modules
                has_modules = False
                for degree_data in uni["degrees"].values():
                    if "modules" in degree_data and degree_data["modules"]:
                        has_modules = True
                        break
                
                if has_modules:
                    # Create a simplified response object
                    uni_data = {
                        "name": uni.get("name", ""),
                        "id": uni.get("id", ""),
                        "students_count": uni.get("counter", 0),
                        "degrees_count": len(uni.get("degrees", {}))
                    }
                    universities_with_data.append(uni_data)
        
        return func.HttpResponse(
            json.dumps(universities_with_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def get_university_degrees(req: func.HttpRequest) -> func.HttpResponse:
    """Get degrees for a specific university with module counts"""
    university_name = req.params.get("university")
    
    if not university_name:
        return func.HttpResponse(
            json.dumps({"error": "University name is required"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        from database import get_university_doc
        university_doc = get_university_doc(university_name)
        
        if not university_doc:
            return func.HttpResponse(
                json.dumps({"error": "University not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        # Get degrees with module counts
        degrees_data = []
        
        if "degrees" in university_doc:
            for degree_name, degree_data in university_doc["degrees"].items():
                module_count = len(degree_data.get("modules", {}))
                
                # Get student count from majors
                student_count = 0
                for major in university_doc.get("majors", []):
                    if major.get("major_name") == degree_name:
                        student_count = major.get("counter", 0)
                        break
                
                if module_count > 0:  # Only include degrees with modules
                    degrees_data.append({
                        "name": degree_name,
                        "modules_count": module_count,
                        "students_count": student_count
                    })
        
        # Add total student count from university
        university_data = {
            "name": university_doc.get("name", ""),
            "students_count": university_doc.get("counter", 0),
            "degrees": degrees_data
        }
        
        return func.HttpResponse(
            json.dumps(university_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def get_degree_modules(req: func.HttpRequest) -> func.HttpResponse:
    """Get all modules for a specific degree with their statistics"""
    university_name = req.params.get("university")
    degree_name = req.params.get("degree")
    
    if not university_name or not degree_name:
        return func.HttpResponse(
            json.dumps({"error": "University and degree names are required"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        modules = get_degree_modules_with_stats(university_name, degree_name)
        
        # Order modules by year and semester
        modules.sort(key=lambda m: (m.get("year", ""), m.get("semester", 0)))
        
        return func.HttpResponse(
            json.dumps({
                "university": university_name,
                "degree": degree_name,
                "modules": modules
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def get_module_details(req: func.HttpRequest) -> func.HttpResponse:
    """Get detailed information about a module including reviews and statistics"""
    module_id = req.params.get("module_id")
    
    if not module_id:
        return func.HttpResponse(
            json.dumps({"error": "Module ID is required"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        # Get module base data
        module = get_module_by_id_public(module_id)
        
        if not module:
            return func.HttpResponse(
                json.dumps({"error": "Module not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        # Get module statistics
        statistics = get_module_statistics(
            module_id, 
            module.get("university", ""), 
            module.get("degree", "")
        )
        
        # Get anonymized reviews
        reviews = get_module_reviews(module_id)
        
        # Anonymize reviews
        anonymous_reviews = []
        for review in reviews:
            anonymous_review = {
                "id": review.get("id"),
                "difficulty_rating": review.get("difficulty_rating"),
                "teaching_quality_rating": review.get("teaching_quality_rating"),
                "recommended_rating": review.get("recommended_rating"),
                "comment": review.get("comment"),
                "grade_received": review.get("grade_received"),
                "created_at": review.get("created_at")
            }
            
            # Only include user email if review is not anonymous
            if not review.get("anonymous", True):
                anonymous_review["user_email"] = review.get("user_email")
                
            anonymous_reviews.append(anonymous_review)
        
        # Create response
        response = {
            "module": module,
            "statistics": statistics,
            "reviews": anonymous_reviews
        }
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def create_module_review_route(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new review for a module - requires authentication"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(
            json.dumps({"error": "Authentication required to submit reviews"}),
            status_code=401,
            mimetype="application/json"
        )
    
    try:
        review_data = req.get_json()
        
        # Validate with model
        try:
            # Add the user's email
            review_data["user_email"] = identity
            
            # Validate with Pydantic model
            review = ModuleReview(**review_data)
            
            # Convert to dict for database
            review_dict = review.dict(exclude_none=True)
            
            # Check if module exists
            module = get_module_by_id_public(review.module_id)
            if not module:
                return func.HttpResponse(
                    json.dumps({"error": "Module not found"}),
                    status_code=404,
                    mimetype="application/json"
                )
            
            # Create review
            created_review = create_module_review(review_dict)
            
            # Return anonymized review
            anonymous_review = {
                "id": created_review.get("id"),
                "module_id": created_review.get("module_id"),
                "difficulty_rating": created_review.get("difficulty_rating"),
                "teaching_quality_rating": created_review.get("teaching_quality_rating"),
                "recommended_rating": created_review.get("recommended_rating"),
                "comment": created_review.get("comment"),
                "grade_received": created_review.get("grade_received"),
                "created_at": created_review.get("created_at")
            }
            
            return func.HttpResponse(
                json.dumps(anonymous_review),
                status_code=201,
                mimetype="application/json"
            )
        except Exception as validation_error:
            return func.HttpResponse(
                json.dumps({"error": f"Validation error: {str(validation_error)}"}),
                status_code=400,
                mimetype="application/json"
            )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def delete_module_review_route(req: func.HttpRequest) -> func.HttpResponse:
    """Delete a module review - requires authentication and must be review owner"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(
            json.dumps({"error": "Authentication required"}),
            status_code=401,
            mimetype="application/json"
        )
    
    review_id = req.route_params.get("id")
    if not review_id:
        return func.HttpResponse(
            json.dumps({"error": "Review ID is required"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        success = delete_module_review(review_id, identity)
        
        if success:
            return func.HttpResponse(
                json.dumps({"message": "Review deleted successfully"}),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                json.dumps({"error": "Review not found or you don't have permission to delete it"}),
                status_code=404,
                mimetype="application/json"
            )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def get_user_reviews(req: func.HttpRequest) -> func.HttpResponse:
    """Get all reviews submitted by the current user - requires authentication"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(
            json.dumps({"error": "Authentication required"}),
            status_code=401,
            mimetype="application/json"
        )
    
    try:
        # Query for reviews by this user
        from database import _container
        
        query = "SELECT * FROM c WHERE c.type = 'module_review' AND c.user_email = @email"
        parameters = [{"name": "@email", "value": identity}]
        
        reviews = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        # Get module info for each review
        enhanced_reviews = []
        
        for review in reviews:
            module = get_module_by_id_public(review.get("module_id"))
            
            if module:
                # Combine review and module data
                enhanced_review = {
                    "id": review.get("id"),
                    "module_id": review.get("module_id"),
                    "module_name": module.get("name"),
                    "module_code": module.get("code"),
                    "university": review.get("university"),
                    "degree": review.get("degree"),
                    "difficulty_rating": review.get("difficulty_rating"),
                    "teaching_quality_rating": review.get("teaching_quality_rating"),
                    "recommended_rating": review.get("recommended_rating"),
                    "comment": review.get("comment"),
                    "grade_received": review.get("grade_received"),
                    "created_at": review.get("created_at")
                }
                
                enhanced_reviews.append(enhanced_review)
        
        return func.HttpResponse(
            json.dumps(enhanced_reviews),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )