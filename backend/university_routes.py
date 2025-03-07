# university_routes.py
import azure.functions as func
import json
import datetime
import uuid
from user_routes import verify_session
from database import get_user_by_email, get_university_doc, _container

def get_university_modules(req: func.HttpRequest) -> func.HttpResponse:
    """Get default modules for a specific university and degree"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get parameters
        university_name = req.params.get('university')
        degree_name = req.params.get('degree')
        
        # If not provided, get from user profile
        if not university_name or not degree_name:
            user_doc = get_user_by_email(identity)
            if not user_doc:
                return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
                
            university_name = user_doc.get("university", "")
            degree_name = user_doc.get("degree", "")
            
        if not university_name or not degree_name:
            return func.HttpResponse(
                json.dumps({"error": "University and degree names are required"}),
                status_code=400
            )
            
        # In a real implementation, this would query a database of university module templates
        # For demonstration, we'll return some example modules for University of Southampton CS
        
        modules = []
        
        if university_name == "University of Southampton" and degree_name == "COMPUTER SCIENCE":
            # Year 1 modules
            modules.extend([
                {
                    "name": "Programming I",
                    "code": "COMP1001",
                    "credits": 15,
                    "year": "Year 1",
                    "semester": 1,
                    "description": "Introduction to programming principles and practices using Python"
                },
                {
                    "name": "Computer Systems I",
                    "code": "COMP1002",
                    "credits": 15,
                    "year": "Year 1",
                    "semester": 1,
                    "description": "Introduction to computer architecture and systems"
                },
                {
                    "name": "Foundations of Computer Science",
                    "code": "COMP1003",
                    "credits": 15,
                    "year": "Year 1",
                    "semester": 1,
                    "description": "Mathematical foundations of computing"
                },
                {
                    "name": "Professional Development",
                    "code": "COMP1004",
                    "credits": 15,
                    "year": "Year 1",
                    "semester": 1,
                    "description": "Development of professional and transferable skills"
                },
                {
                    "name": "Data Structures and Algorithms",
                    "code": "COMP1005",
                    "credits": 15,
                    "year": "Year 1",
                    "semester": 2,
                    "description": "Study of fundamental data structures and algorithms"
                },
                {
                    "name": "Web Development",
                    "code": "COMP1006",
                    "credits": 15,
                    "year": "Year 1",
                    "semester": 2,
                    "description": "Design and implementation of web-based applications"
                }
            ])
            
            # Year 2 modules
            modules.extend([
                {
                    "name": "Programming II",
                    "code": "COMP2001",
                    "credits": 15,
                    "year": "Year 2",
                    "semester": 1,
                    "description": "Advanced programming concepts using Java"
                },
                {
                    "name": "Software Engineering",
                    "code": "COMP2002",
                    "credits": 15,
                    "year": "Year 2",
                    "semester": 1,
                    "description": "Software development methodologies and practices"
                },
                {
                    "name": "Intelligent Systems",
                    "code": "COMP2003",
                    "credits": 15,
                    "year": "Year 2",
                    "semester": 1,
                    "description": "Introduction to artificial intelligence and machine learning"
                },
                {
                    "name": "Computer Networks",
                    "code": "COMP2004",
                    "credits": 15,
                    "year": "Year 2",
                    "semester": 2,
                    "description": "Principles and practice of computer networking"
                },
                {
                    "name": "Distributed Systems",
                    "code": "COMP2005",
                    "credits": 15,
                    "year": "Year 2",
                    "semester": 2,
                    "description": "Design and implementation of distributed computing systems"
                }
            ])
            
            # Year 3 modules
            modules.extend([
                {
                    "name": "Final Year Project",
                    "code": "COMP3001",
                    "credits": 30,
                    "year": "Year 3",
                    "semester": 1,
                    "description": "Individual research and development project"
                },
                {
                    "name": "Cybersecurity",
                    "code": "COMP3002",
                    "credits": 15,
                    "year": "Year 3",
                    "semester": 1,
                    "description": "Security principles and practices in computing"
                },
                {
                    "name": "Data Mining",
                    "code": "COMP3003",
                    "credits": 15,
                    "year": "Year 3",
                    "semester": 1,
                    "description": "Techniques for knowledge discovery in databases"
                },
                {
                    "name": "Advanced Databases",
                    "code": "COMP3004",
                    "credits": 15,
                    "year": "Year 3",
                    "semester": 2,
                    "description": "Advanced concepts in database management systems"
                },
                {
                    "name": "Computer Vision",
                    "code": "COMP3005",
                    "credits": 15,
                    "year": "Year 3",
                    "semester": 2,
                    "description": "Theory and applications of computer vision"
                }
            ])
        
        # Group modules by year and semester
        organized = {}
        
        for module in modules:
            year = module.get("year")
            semester = module.get("semester")
            
            if year not in organized:
                organized[year] = {}
                
            if semester not in organized[year]:
                organized[year][semester] = []
                
            organized[year][semester].append(module)
        
        return func.HttpResponse(json.dumps(organized), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def get_degree_requirements(req: func.HttpRequest) -> func.HttpResponse:
    """Get degree requirements for a specific university and program"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get parameters
        university_name = req.params.get('university')
        degree_name = req.params.get('degree')
        
        # If not provided, get from user profile
        if not university_name or not degree_name:
            user_doc = get_user_by_email(identity)
            if not user_doc:
                return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
                
            university_name = user_doc.get("university", "")
            degree_name = user_doc.get("degree", "")
            
        if not university_name or not degree_name:
            return func.HttpResponse(
                json.dumps({"error": "University and degree names are required"}),
                status_code=400
            )
            
        # For demonstration, return example requirements for Computer Science at Southampton
        requirements = {
            "totalCredits": 360,  # 120 per year for 3 years
            "requiredModules": [
                {"code": "COMP1001", "name": "Programming I", "year": "Year 1"},
                {"code": "COMP1003", "name": "Foundations of Computer Science", "year": "Year 1"},
                {"code": "COMP1005", "name": "Data Structures and Algorithms", "year": "Year 1"},
                {"code": "COMP2001", "name": "Programming II", "year": "Year 2"},
                {"code": "COMP2002", "name": "Software Engineering", "year": "Year 2"},
                {"code": "COMP3001", "name": "Final Year Project", "year": "Year 3"}
            ],
            "optionalCredits": {
                "Year 1": 45,
                "Year 2": 90,
                "Year 3": 90
            },
            "minimumGradeRequirements": {
                "overall": 40,
                "majorSubjects": 40,
                "finalProject": 40
            },
            "yearWeights": {
                "Year 1": 0,   # Year 1 typically doesn't count in UK universities
                "Year 2": 40,  # 40% of final grade
                "Year 3": 60   # 60% of final grade
            }
        }
        
        return func.HttpResponse(json.dumps(requirements), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def import_template_modules(req: func.HttpRequest) -> func.HttpResponse:
    """Import template modules for a year/semester into the user's account"""
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(json.dumps({"error": identity}), status_code=401)

    try:
        # Get parameters from request body
        params = req.get_json()
        year = params.get("year")
        semester = params.get("semester")
        
        if not year:
            return func.HttpResponse(
                json.dumps({"error": "Year parameter is required"}),
                status_code=400
            )
            
        # Get user details
        user_doc = get_user_by_email(identity)
        if not user_doc:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404)
            
        university_name = user_doc.get("university", "")
        degree_name = user_doc.get("degree", "")
        
        if not university_name or not degree_name:
            return func.HttpResponse(
                json.dumps({"error": "User must have university and degree set in profile"}),
                status_code=400
            )
            
        # Get template modules
        # In a real implementation, this would query a database of university module templates
        # For demonstration, we use the same example modules as in get_university_modules
        
        modules = []
        
        if university_name == "University of Southampton" and degree_name == "COMPUTER SCIENCE":
            # Filter for requested year
            if year == "Year 1":
                modules.extend([
                    {
                        "name": "Programming I",
                        "code": "COMP1001",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 1,
                        "description": "Introduction to programming principles and practices using Python"
                    },
                    {
                        "name": "Computer Systems I",
                        "code": "COMP1002",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 1,
                        "description": "Introduction to computer architecture and systems"
                    },
                    {
                        "name": "Foundations of Computer Science",
                        "code": "COMP1003",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 1,
                        "description": "Mathematical foundations of computing"
                    },
                    {
                        "name": "Professional Development",
                        "code": "COMP1004",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 1,
                        "description": "Development of professional and transferable skills"
                    },
                    {
                        "name": "Data Structures and Algorithms",
                        "code": "COMP1005",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 2,
                        "description": "Study of fundamental data structures and algorithms"
                    },
                    {
                        "name": "Web Development",
                        "code": "COMP1006",
                        "credits": 15,
                        "year": "Year 1",
                        "semester": 2,
                        "description": "Design and implementation of web-based applications"
                    }
                ])
            elif year == "Year 2":
                modules.extend([
                    {
                        "name": "Programming II",
                        "code": "COMP2001",
                        "credits": 15,
                        "year": "Year 2",
                        "semester": 1,
                        "description": "Advanced programming concepts using Java"
                    },
                    {
                        "name": "Software Engineering",
                        "code": "COMP2002",
                        "credits": 15,
                        "year": "Year 2",
                        "semester": 1,
                        "description": "Software development methodologies and practices"
                    },
                    {
                        "name": "Intelligent Systems",
                        "code": "COMP2003",
                        "credits": 15,
                        "year": "Year 2",
                        "semester": 1,
                        "description": "Introduction to artificial intelligence and machine learning"
                    },
                    {
                        "name": "Computer Networks",
                        "code": "COMP2004",
                        "credits": 15,
                        "year": "Year 2",
                        "semester": 2,
                        "description": "Principles and practice of computer networking"
                    },
                    {
                        "name": "Distributed Systems",
                        "code": "COMP2005",
                        "credits": 15,
                        "year": "Year 2",
                        "semester": 2,
                        "description": "Design and implementation of distributed computing systems"
                    }
                ])
            elif year == "Year 3":
                modules.extend([
                    {
                        "name": "Final Year Project",
                        "code": "COMP3001",
                        "credits": 30,
                        "year": "Year 3",
                        "semester": 1,
                        "description": "Individual research and development project"
                    },
                    {
                        "name": "Cybersecurity",
                        "code": "COMP3002",
                        "credits": 15,
                        "year": "Year 3",
                        "semester": 1,
                        "description": "Security principles and practices in computing"
                    },
                    {
                        "name": "Data Mining",
                        "code": "COMP3003",
                        "credits": 15,
                        "year": "Year 3",
                        "semester": 1,
                        "description": "Techniques for knowledge discovery in databases"
                    },
                    {
                        "name": "Advanced Databases",
                        "code": "COMP3004",
                        "credits": 15,
                        "year": "Year 3",
                        "semester": 2,
                        "description": "Advanced concepts in database management systems"
                    },
                    {
                        "name": "Computer Vision",
                        "code": "COMP3005",
                        "credits": 15,
                        "year": "Year 3",
                        "semester": 2,
                        "description": "Theory and applications of computer vision"
                    }
                ])
        
        # Further filter by semester if requested
        if semester:
            semester = int(semester)
            modules = [m for m in modules if m.get("semester") == semester]
            
        # Add the modules to the user's account
        imported_count = 0
        
        for template in modules:
            # Create module object
            module_data = {
                "id": str(uuid.uuid4()),
                "user_email": identity,
                "type": "module",
                "name": template.get("name"),
                "code": template.get("code"),
                "credits": template.get("credits"),
                "year": template.get("year"),
                "semester": template.get("semester"),
                "university": university_name,
                "degree": degree_name,
                "description": template.get("description"),
                "status": "active",
                "score": 0,  # Default score
                "assessments": [
                    {
                        "name": "Coursework",
                        "weight": 40,
                        "score": 0
                    },
                    {
                        "name": "Final Exam",
                        "weight": 60,
                        "score": 0
                    }
                ],
                "created_at": datetime.datetime.utcnow().isoformat(),
                "updated_at": datetime.datetime.utcnow().isoformat()
            }
            
            # Create in database
            _container.create_item(body=module_data)
            imported_count += 1
            
        # Add activity
        if imported_count > 0:
            # Get user doc again
            user_doc = get_user_by_email(identity)
            
            # Initialize dashboardConfig if needed
            if "dashboardConfig" not in user_doc:
                user_doc["dashboardConfig"] = {}
                
            # Initialize recentActivities if needed
            if "recentActivities" not in user_doc["dashboardConfig"]:
                user_doc["dashboardConfig"]["recentActivities"] = []
                
            # Add activity
            activity = {
                "type": "import",
                "title": "Modules Imported",
                "description": f"Imported {imported_count} modules for {year}" + (f", Semester {semester}" if semester else ""),
                "time": "Just now"
            }
            
            # Add to beginning of list
            user_doc["dashboardConfig"]["recentActivities"].insert(0, activity)
            
            # Limit to 10 activities
            user_doc["dashboardConfig"]["recentActivities"] = user_doc["dashboardConfig"]["recentActivities"][:10]
            
            # Update user document
            _container.upsert_item(user_doc)
        
        return func.HttpResponse(
            json.dumps({
                "message": f"Successfully imported {imported_count} modules",
                "importedCount": imported_count
            }),
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)