import json
import azure.functions as func
from database import get_user_by_email, _container, get_university_doc, get_user_modules
from user_routes import verify_session
from database import update_university_module_data, search_modules_for_university, get_user_by_email, get_user_modules
from models import Module, Assessment, Examination
import uuid
from datetime import datetime
from database import increment_university_and_major_counter, get_modules_with_stats




def get_all_modules(req: func.HttpRequest) -> func.HttpResponse:
    """Get all modules for the current user with optional filtering"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get optional query parameters for filtering
        year = req.params.get('year')
        semester = req.params.get('semester')
        status = req.params.get('status')

        # Start with base query
        query = "SELECT * FROM c WHERE c.type = 'module' AND c.user_email = @email"
        parameters = [{"name": "@email", "value": identity}]

        # Add filters if provided
        if year:
            query += " AND c.year = @year"
            parameters.append({"name": "@year", "value": year})
        
        if semester:
            query += " AND c.semester = @semester"
            parameters.append({"name": "@semester", "value": int(semester)})
        
        if status:
            query += " AND c.status = @status"
            parameters.append({"name": "@status", "value": status})

        # Execute query
        modules = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        return func.HttpResponse(json.dumps(modules), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_module(req: func.HttpRequest) -> func.HttpResponse:
    """Get a specific module by ID"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    module_id = req.route_params.get('id')
    if not module_id:
        return func.HttpResponse(json.dumps({"error": "Module ID is required"}), status_code=400)

    try:
        # Query specifically with partition key and user check
        query = "SELECT * FROM c WHERE c.id = @id AND c.user_email = @email AND c.type = 'module'"
        parameters = [
            {"name": "@id", "value": module_id},
            {"name": "@email", "value": identity}
        ]

        modules = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        if not modules:
            return func.HttpResponse(json.dumps({"error": "Module not found or access denied"}), status_code=404)

        return func.HttpResponse(json.dumps(modules[0]), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def delete_module(req: func.HttpRequest) -> func.HttpResponse:
    """Delete a module"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    module_id = req.route_params.get('id')
    if not module_id:
        return func.HttpResponse(json.dumps({"error": "Module ID is required"}), status_code=400)

    try:
        # Verify ownership and get module details before deletion
        query = "SELECT * FROM c WHERE c.id = @id AND c.user_email = @email AND c.type = 'module'"
        parameters = [
            {"name": "@id", "value": module_id},
            {"name": "@email", "value": identity}
        ]

        existing_modules = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        if not existing_modules:
            return func.HttpResponse(json.dumps({"error": "Module not found or access denied"}), status_code=404)
        
        module_to_delete = existing_modules[0]
        
        # Add activity for module deletion
        module_obj = Module(**module_to_delete)
        add_module_activity(identity, module_obj, "Module Deleted")

        # Delete from database
        _container.delete_item(item=module_id, partition_key=module_id)
        
        return func.HttpResponse(json.dumps({"message": "Module deleted successfully"}), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)

def add_module_activity(user_email, module, activity_type):
    """Add an activity related to module changes to the user's dashboard"""
    try:
        user_doc = get_user_by_email(user_email)
        
        if not user_doc:
            return
            
        # Initialize dashboardConfig if it doesn't exist
        if "dashboardConfig" not in user_doc:
            user_doc["dashboardConfig"] = {}
            
        # Initialize recentActivities if it doesn't exist
        if "recentActivities" not in user_doc["dashboardConfig"]:
            user_doc["dashboardConfig"]["recentActivities"] = []
            
        # Create activity item
        activity = {
            "type": "grade",  # grade type for module-related activities
            "title": activity_type,
            "description": f"{module.name}: {module.score}%",
            "time": "Just now"
        }
        
        # Insert activity at the beginning of the list
        user_doc["dashboardConfig"]["recentActivities"].insert(0, activity)
        
        # Limit list to 10 most recent activities
        user_doc["dashboardConfig"]["recentActivities"] = \
            user_doc["dashboardConfig"]["recentActivities"][:10]
            
        # Update user document
        _container.upsert_item(user_doc)
        
    except Exception as e:
        print(f"Error adding module activity: {str(e)}")
        # Log error but don't stop the main operation

def get_modules_by_year_semester(req: func.HttpRequest) -> func.HttpResponse:
    """Get modules organized by year and semester"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get all modules for the user
        query = "SELECT * FROM c WHERE c.type = 'module' AND c.user_email = @email"
        parameters = [{"name": "@email", "value": identity}]

        modules = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        # Organize modules by year and semester
        organized = {}
        
        for module in modules:
            year = module.get("year", "Unknown")
            semester = module.get("semester", 1)
            
            if year not in organized:
                organized[year] = {}
                
            if semester not in organized[year]:
                organized[year][semester] = []
                
            organized[year][semester].append(module)
        
        return func.HttpResponse(json.dumps(organized), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)


# Update the get_module_suggestions function in module_routes.py

def get_module_suggestions(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get module suggestions based on partial text input.
    Searches modules at the user's university that match the text.
    """
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get search query parameter
        query = req.params.get('query')
        if not query or len(query) < 2:  # Require at least 2 characters
            return func.HttpResponse(
                json.dumps({"error": "Query parameter must be at least 2 characters"}),
                status_code=400
            )
            
        # Get university and degree - first try query parameters
        university = req.params.get('university')
        user_degree = req.params.get('degree')
        
        # If not provided in query, get from user profile
        if not university or not user_degree:
            user_doc = get_user_by_email(identity)
            if not user_doc:
                return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
                
            if not university:
                university = user_doc.get("university", "")
            if not user_degree:
                user_degree = user_doc.get("degree", "")
        
        if not university:
            return func.HttpResponse(
                json.dumps({"error": "University is required, either in query parameters or user profile"}),
                status_code=400
            )

        # Detailed logging to help debug
        print(f"Searching for modules with query '{query}'")
        print(f"University: '{university}', Degree: '{user_degree}'")

        # Get module suggestions from database
        from database import search_modules_for_university
        modules = search_modules_for_university(university, query)
        
        # Fallback sample data if no modules found
        if not modules and university == "University of Southampton" and "COMPUTER" in user_degree:
            print("No modules found. Using fallback sample data.")
            if "pro" in query.lower():
                modules = [
                    {
                        "id": "comp1001",
                        "name": "Programming I",
                        "code": "COMP1001",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 1,
                        "university": university,
                        "degree": user_degree,
                        "description": "Introduction to programming principles and practices using Python"
                    },
                    {
                        "id": "comp1002",
                        "name": "Programming II",
                        "code": "COMP1002",
                        "credits": 15,
                        "year": "Year 2",
                        "semester": 1,
                        "university": university,
                        "degree": user_degree,
                        "description": "Advanced programming concepts using Java"
                    }
                ]
        
        # Flag modules that belong to the user's degree
        for module in modules:
            module["in_user_degree"] = (module.get("degree") == user_degree)
        
        # Create response with grouped suggestions
        user_degree_modules = [m for m in modules if m.get("in_user_degree")]
        other_modules = [m for m in modules if not m.get("in_user_degree")]
        
        suggestions = {
            "user_degree_modules": user_degree_modules,
            "other_modules": other_modules
        }
        
        print(f"Returning {len(user_degree_modules)} modules in user's degree and {len(other_modules)} modules from other degrees")
        
        return func.HttpResponse(json.dumps(suggestions), status_code=200)
    except Exception as e:
        print(f"Error getting module suggestions: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)
                                 

def get_module_analytics(req: func.HttpRequest) -> func.HttpResponse:
    """Get analytics data for modules from the same university and degree"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get user information
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
        
        university = user_doc.get("university", "")
        degree = user_doc.get("degree", "")
        
        if not university or not degree:
            return func.HttpResponse(
                json.dumps({"error": "University and degree information required"}),
                status_code=400
            )
        
        # Get module statistics
        module_stats = get_modules_with_stats(university, degree)
        
        # Get user's modules for comparison
        user_modules = get_user_modules(identity)
        user_module_dict = {m.get("name", ""): m for m in user_modules}
        
        # Add user's score to each module for comparison
        for stat in module_stats:
            module_name = stat.get("name", "")
            if module_name in user_module_dict:
                stat["yourScore"] = user_module_dict[module_name].get("score", 0)
                stat["difference"] = stat["yourScore"] - stat.get("average_score", 0)
            else:
                stat["yourScore"] = None
                stat["difference"] = None
        
        return func.HttpResponse(json.dumps(module_stats), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def create_module(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new module with normalization and duplicate checking"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get user data to pre-populate university and degree if not provided
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)

        # Get module data from request
        module_data = req.get_json()

        module_data["user_email"] = identity
        module_data["type"] = "module"

        # Auto-populate university and degree if not provided
        if "university" not in module_data:
            module_data["university"] = user_doc.get("university", "")

        if "degree" not in module_data:
            module_data["degree"] = user_doc.get("degree", "")

        # Add user email and type
        module_data["user_email"] = identity
        module_data["type"] = "module"

        # Generate ID if not provided
        if "id" not in module_data:
            module_data["id"] = str(uuid.uuid4())

        # Set creation and update timestamps
        now = datetime.utcnow().isoformat()
        module_data["created_at"] = now
        module_data["updated_at"] = now

        # Convert examination data if provided
        if "examination" in module_data and module_data["examination"]:
            examination_data = module_data["examination"]
            module_data["examination"] = Examination(**examination_data).dict()

        # Validate with model
        module = Module(**module_data)

        # Calculate overall score based on assessments and examination
        total_weighted_score = 0
        total_weight = 0

        # Process assessments
        for assessment in module.assessments:
            assessment_weight = assessment.weight
            total_weighted_score += assessment.score * assessment_weight
            total_weight += assessment_weight

        # Process examination if present
        if module.examination:
            exam_weight = module.examination.weight
            total_weighted_score += module.examination.score * exam_weight
            total_weight += exam_weight

        # Calculate final score if weights are present
        if total_weight > 0:
            module.score = round(total_weighted_score / total_weight, 1)

        # Create module in database
        result = _container.create_item(body=module.dict(exclude_none=True))

        # Update module statistics in university analytics
        if module.university and module.degree and module.score is not None:
            try:
                update_university_module_data({
                    "university": module.university,
                    "degree": module.degree,
                    "name": module.name,
                    "code": module.code,
                    "score": module.score
                })
            except Exception as e:
                # Log error but don't fail the request
                print(f"Error updating university module data: {str(e)}")

        # Add activity to user's dashboard
        add_module_activity(identity, module, "Module Added")

        return func.HttpResponse(json.dumps(result), status_code=201)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)
    

def update_module(req: func.HttpRequest) -> func.HttpResponse:
    """Update an existing module"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    module_id = req.route_params.get('id')
    if not module_id:
        return func.HttpResponse(json.dumps({"error": "Module ID is required"}), status_code=400)

    try:
        module_data = req.get_json()

        # Verify ownership
        query = "SELECT * FROM c WHERE c.id = @id AND c.user_email = @email AND c.type = 'module'"
        parameters = [
            {"name": "@id", "value": module_id},
            {"name": "@email", "value": identity}
        ]

        existing_modules = list(_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        if not existing_modules:
            return func.HttpResponse(json.dumps({"error": "Module not found or access denied"}), status_code=404)

        existing_module = existing_modules[0]
        
        # Store old score for analytics updates
        old_score = existing_module.get("score", 0)
        
        # Update timestamp
        module_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Preserve creation timestamp if exists
        if "created_at" in existing_module:
            module_data["created_at"] = existing_module["created_at"]
        
        # Update fields while preserving id, user_email, and type
        for key, value in module_data.items():
            if key not in ['id', 'user_email', 'type', 'created_at']:
                existing_module[key] = value

        # Process examination data if updated
        if "examination" in module_data and module_data["examination"]:
            existing_module["examination"] = Examination(**module_data["examination"]).dict()

        # Calculate overall score based on assessments and examination
        total_weighted_score = 0
        total_weight = 0
        
        # Process assessments
        for assessment in existing_module.get("assessments", []):
            assessment_weight = assessment.get("weight", 0)
            total_weighted_score += assessment.get("score", 0) * assessment_weight
            total_weight += assessment_weight
            
        # Process examination if present
        examination = existing_module.get("examination")
        if examination:
            exam_weight = examination.get("weight", 0)
            total_weighted_score += examination.get("score", 0) * exam_weight
            total_weight += exam_weight
            
        # Calculate final score if weights are present
        if total_weight > 0:
            existing_module["score"] = round(total_weighted_score / total_weight, 1)

        # Update in database
        result = _container.replace_item(item=module_id, body=existing_module)
        
        # Update module statistics in university analytics
        if "university" in existing_module and "degree" in existing_module:
            try:
                update_university_module_data({
                    "university": existing_module["university"],
                    "degree": existing_module["degree"],
                    "name": existing_module["name"],
                    "code": existing_module.get("code", ""),
                    "score": existing_module["score"],
                    "is_update": True,
                    "old_score": old_score
                })
            except Exception as e:
                # Log error but don't fail the request
                print(f"Error updating university module data: {str(e)}")
        
        # Add activity for module update
        module_obj = Module(**existing_module)
        add_module_activity(identity, module_obj, "Module Updated")
        
        return func.HttpResponse(json.dumps(result), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=400)