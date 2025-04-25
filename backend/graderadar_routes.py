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
    get_module_by_id_public,
    _container
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

# New functions to add
def search_modules(req: func.HttpRequest) -> func.HttpResponse:
    """Search for modules across universities based on query parameters"""
    try:
        # Get query parameters
        query = req.params.get("query")
        university = req.params.get("university")
        limit = int(req.params.get("limit", "20"))
        
        if not query and not university:
            return func.HttpResponse(
                json.dumps({"error": "Either 'query' or 'university' parameter is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Query for modules matching criteria
        from database import search_modules_for_university
        results = []
        
        if university:
            # If university is specified, search within that university
            results = search_modules_for_university(university, query, limit)
        else:
            # If no university specified, search across top universities
            from database import get_all_universities_docs
            universities = get_all_universities_docs()
            # Limit to top 5 universities for performance
            top_universities = sorted(universities, key=lambda u: u.get("counter", 0), reverse=True)[:5]
            
            for uni in top_universities:
                uni_results = search_modules_for_university(uni.get("name", ""), query, limit // 5)
                results.extend(uni_results)
                # Break early if we have enough results
                if len(results) >= limit:
                    break
            
            # Sort by relevance
            results = sorted(results, key=lambda m: 
                0 if query.lower() in (m.get("name", "") + m.get("code", "")).lower() else 1
            )[:limit]
        
        return func.HttpResponse(
            json.dumps(results),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def create_module(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new module in the GradeRadar system (not user-specific)"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        module_data = req.get_json()
        
        # Validate required fields
        required_fields = ['name', 'code', 'university', 'degree', 'credits', 'year', 'semester']
        for field in required_fields:
            if field not in module_data:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400,
                    mimetype="application/json"
                )
        
        # Check if similar module already exists
        from database import check_similar_module_exists
        existing_module = check_similar_module_exists(
            module_data.get("university"),
            module_data.get("degree"),
            module_data.get("name"),
            module_data.get("code")
        )
        
        if existing_module:
            return func.HttpResponse(
                json.dumps({
                    "error": "Similar module already exists",
                    "existing_module": existing_module
                }),
                status_code=409,  # Conflict
                mimetype="application/json"
            )
        
        # Normalize module name
        from database import normalize_module_name
        module_data["name"] = normalize_module_name(module_data.get("name", ""))
        
        # Add metadata
        module_data["id"] = f"module_{str(uuid.uuid4())}"
        module_data["type"] = "module"
        module_data["created_by"] = identity
        module_data["created_at"] = datetime.datetime.utcnow().isoformat()
        module_data["updated_at"] = datetime.datetime.utcnow().isoformat()
        module_data["review_count"] = 0
        module_data["avg_rating"] = 0.0
        
        # Create in database
        result = _container.create_item(body=module_data)
        
        # Update university module data
        from module_routes import update_university_module_data
        update_university_module_data(module_data)
        
        return func.HttpResponse(
            json.dumps(result),
            status_code=201,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def update_module(req: func.HttpRequest) -> func.HttpResponse:
    """Update a module in the GradeRadar system"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    module_id = req.route_params.get('id')
    if not module_id:
        return func.HttpResponse(
            json.dumps({"error": "Module ID is required"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        module_data = req.get_json()
        
        # Get existing module
        query = "SELECT * FROM c WHERE c.id = @id AND c.type = 'module'"
        parameters = [{"name": "@id", "value": module_id}]
        
        modules = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        if not modules:
            return func.HttpResponse(
                json.dumps({"error": "Module not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        existing_module = modules[0]
        
        # Check if user is authorized to update this module
        # Only creator or admin can update
        if existing_module.get("created_by") != identity:
            # In a real app, you might check if the user is an admin here
            return func.HttpResponse(
                json.dumps({"error": "You are not authorized to update this module"}),
                status_code=403,
                mimetype="application/json"
            )
        
        # Update fields
        for key, value in module_data.items():
            if key not in ["id", "type", "created_by", "created_at"]:
                existing_module[key] = value
        
        # Update timestamp
        existing_module["updated_at"] = datetime.datetime.utcnow().isoformat()
        
        # Save changes
        result = _container.replace_item(item=module_id, body=existing_module)
        
        # Update university module data
        from module_routes import update_university_module_data
        update_university_module_data(existing_module)
        
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def get_user_profile(req: func.HttpRequest) -> func.HttpResponse:
    """Get GradeRadar profile for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        # Get user document
        from database import get_user_by_email
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(
                json.dumps({"error": "User not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        # Extract GradeRadar profile information
        profile = {
            "email": identity,
            "display_name": user_doc.get("graderadar_display_name", user_doc.get("firstName", "")),
            "university": user_doc.get("university", ""),
            "degree": user_doc.get("degree", ""),
            "graduation_year": user_doc.get("graduation_year", ""),
            "show_name_in_reviews": user_doc.get("graderadar_show_name", False),
            "receive_notifications": user_doc.get("graderadar_notifications", True),
            "created_at": user_doc.get("graderadar_created_at", user_doc.get("createdAt", "")),
            "review_count": get_user_review_count(identity),
            "contribution_score": calculate_contribution_score(identity)
        }
        
        return func.HttpResponse(
            json.dumps(profile),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def update_user_profile(req: func.HttpRequest) -> func.HttpResponse:
    """Update GradeRadar profile for the current user"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)
    
    try:
        profile_data = req.get_json()
        
        # Get user document
        from database import get_user_by_email
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(
                json.dumps({"error": "User not found"}),
                status_code=404,
                mimetype="application/json"
            )
        
        # Update GradeRadar specific fields
        if "display_name" in profile_data:
            user_doc["graderadar_display_name"] = profile_data["display_name"]
        
        if "show_name_in_reviews" in profile_data:
            user_doc["graderadar_show_name"] = profile_data["show_name_in_reviews"]
            
        if "receive_notifications" in profile_data:
            user_doc["graderadar_notifications"] = profile_data["receive_notifications"]
            
        if "graduation_year" in profile_data:
            user_doc["graduation_year"] = profile_data["graduation_year"]
        
        # Set creation timestamp if not already set
        if "graderadar_created_at" not in user_doc:
            user_doc["graderadar_created_at"] = datetime.datetime.utcnow().isoformat()
        
        # Save changes
        _container.upsert_item(user_doc)
        
        # Return updated profile
        updated_profile = {
            "email": identity,
            "display_name": user_doc.get("graderadar_display_name", user_doc.get("firstName", "")),
            "university": user_doc.get("university", ""),
            "degree": user_doc.get("degree", ""),
            "graduation_year": user_doc.get("graduation_year", ""),
            "show_name_in_reviews": user_doc.get("graderadar_show_name", False),
            "receive_notifications": user_doc.get("graderadar_notifications", True),
            "created_at": user_doc.get("graderadar_created_at", ""),
            "review_count": get_user_review_count(identity),
            "contribution_score": calculate_contribution_score(identity)
        }
        
        return func.HttpResponse(
            json.dumps(updated_profile),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# Helper functions for GradeRadar profiles

def get_user_review_count(user_email: str) -> int:
    """Get the number of reviews created by a user"""
    try:
        query = "SELECT COUNT(1) as count FROM c WHERE c.type = 'module_review' AND c.user_email = @email"
        parameters = [{"name": "@email", "value": user_email}]
        
        results = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return results[0].get("count", 0) if results else 0
    except Exception:
        return 0

def calculate_contribution_score(user_email: str) -> int:
    """Calculate the user's contribution score based on activity"""
    try:
        # Get user's review count
        review_count = get_user_review_count(user_email)
        
        # Get count of modules created by user
        query = "SELECT COUNT(1) as count FROM c WHERE c.type = 'module' AND c.created_by = @email"
        parameters = [{"name": "@email", "value": user_email}]
        
        results = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        module_count = results[0].get("count", 0) if results else 0
        
        # Calculate score: reviews are worth 5 points, modules are worth 10 points
        score = (review_count * 5) + (module_count * 10)
        
        return score
    except Exception:
        return 0

def test_graderadar_integration(req: func.HttpRequest) -> func.HttpResponse:
    """Test endpoint to verify GradeRadar integration is working"""
    try:
        # Get current API status
        from database import get_newest_reviews, get_popular_modules, get_top_contributors
        
        # Test getting newest reviews (limit to 3 for quick test)
        newest_reviews = get_newest_reviews(3)
        
        # Test getting popular modules for a sample university
        popular_modules = get_popular_modules("University of Southampton", limit=3)
        
        # Test getting top contributors
        top_contributors = get_top_contributors(3)
        
        # Return test results
        test_results = {
            "status": "operational",
            "endpoints_available": [
                "/api/graderadar/universities",
                "/api/graderadar/university/degrees",
                "/api/graderadar/modules",
                "/api/graderadar/module",
                "/api/graderadar/search/modules",
                "/api/graderadar/reviews",
                "/api/graderadar/user/reviews",
                "/api/graderadar/user/profile"
            ],
            "sample_data": {
                "newest_reviews_count": len(newest_reviews),
                "newest_reviews": newest_reviews,
                "popular_modules_count": len(popular_modules),
                "popular_modules": popular_modules,
                "top_contributors_count": len(top_contributors),
                "top_contributors": top_contributors
            }
        }
        
        return func.HttpResponse(
            json.dumps(test_results),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "GradeRadar integration test failed",
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )