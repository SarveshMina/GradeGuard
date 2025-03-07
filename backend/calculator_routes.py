#calculator_routes.py

import azure.functions as func
import json

def update_calculator_config(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        return func.HttpResponse(json.dumps({"message": "Calculator updated"}), status_code=200)
    except ValueError:
        return func.HttpResponse("Invalid request body", status_code=400)

def get_calculator_config(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({"message": "Calculator config"}), status_code=200) 