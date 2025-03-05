import json
import azure.functions as func
from database import _container
from user_routes import verify_session

def get_modules(req: func.HttpRequest) -> func.HttpResponse:
    # Verify session
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(
            json.dumps({"error": identity}),
            status_code=401,
            mimetype="application/json"
        )
    
    # Query modules for the user
    query = f"SELECT * FROM c WHERE c.type = 'module' AND c.userEmail = '{identity}'"
    items = list(_container.query_items(query=query, enable_cross_partition_query=True))
    
    return func.HttpResponse(
        json.dumps(items),
        status_code=200,
        mimetype="application/json"
    )

def create_or_update_module(req: func.HttpRequest) -> func.HttpResponse:
    # Verify session
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(
            json.dumps({"error": identity}),
            status_code=401,
            mimetype="application/json"
        )
    
    # Get module data from request
    module_data = req.get_json()
    module_data["type"] = "module"
    module_data["userEmail"] = identity
    
    # Check if this is an update (has id) or create
    if "id" in module_data:
        # First verify the module belongs to this user
        query = f"SELECT * FROM c WHERE c.id = '{module_data['id']}' AND c.userEmail = '{identity}'"
        items = list(_container.query_items(query=query, enable_cross_partition_query=True))
        if not items:
            return func.HttpResponse(
                json.dumps({"error": "Module not found or access denied"}),
                status_code=404,
                mimetype="application/json"
            )
        # Update existing module
        _container.upsert_item(module_data)
    else:
        # Create new module
        response = _container.create_item(body=module_data)
        module_data["id"] = response["id"]
    
    return func.HttpResponse(
        json.dumps(module_data),
        status_code=200,
        mimetype="application/json"
    )

def delete_module(req: func.HttpRequest) -> func.HttpResponse:
    # Verify session
    is_valid, identity = verify_session(req)
    if not is_valid:
        return func.HttpResponse(
            json.dumps({"error": identity}),
            status_code=401,
            mimetype="application/json"
        )
    
    # Get module ID from route
    module_id = req.route_params.get("id")
    if not module_id:
        return func.HttpResponse(
            json.dumps({"error": "Module ID is required"}),
            status_code=400,
            mimetype="application/json"
        )
    
    # Verify module belongs to user
    query = f"SELECT * FROM c WHERE c.id = '{module_id}' AND c.userEmail = '{identity}'"
    items = list(_container.query_items(query=query, enable_cross_partition_query=True))
    if not items:
        return func.HttpResponse(
            json.dumps({"error": "Module not found or access denied"}),
            status_code=404,
            mimetype="application/json"
        )
    
    # Delete the module
    _container.delete_item(item=module_id, partition_key=module_id)
    
    return func.HttpResponse(
        json.dumps({"message": "Module deleted successfully"}),
        status_code=200,
        mimetype="application/json"
    )