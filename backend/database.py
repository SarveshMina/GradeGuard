# database.py

import os
from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DBNAME = os.environ.get("COSMOS_DBNAME")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER")  # e.g., "users"
COSMOS_UNI_CONTAINER = os.environ.get("COSMOS_UNI_CONTAINER")  # e.g. "universities"

_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
_db = _client.get_database_client(COSMOS_DBNAME)

_container = _db.get_container_client(COSMOS_CONTAINER)
_uni_container = _db.get_container_client(COSMOS_UNI_CONTAINER)

def create_user(user_dict: dict):
    _container.create_item(user_dict)

def get_user_by_email(email: str):
    try:
        user_doc = _container.read_item(item=email, partition_key=email)
        return user_doc
    except Exception:
        return None

def increment_university_and_major_counter(university_name: str, major_name: str):
    try:
        uni_doc = _uni_container.read_item(item=university_name, partition_key=university_name)
    except:
        uni_doc = {
            "id": university_name,
            "name": university_name,
            "counter": 0,
            "majors": []
        }
    uni_doc["counter"] = uni_doc.get("counter", 0) + 1

    major_found = None
    for m in uni_doc["majors"]:
        if m["major_name"].lower() == major_name.lower():
            major_found = m
            break

    if major_found:
        major_found["counter"] += 1
    else:
        uni_doc["majors"].append({
            "major_name": major_name,
            "counter": 1
        })

    _uni_container.upsert_item(uni_doc)

def get_all_universities_docs():
    query = "SELECT * FROM c"
    items = list(_uni_container.query_items(query=query, enable_cross_partition_query=True))
    return items

def get_university_doc(university_name: str):
    try:
        doc = _uni_container.read_item(item=university_name, partition_key=university_name)
        return doc
    except:
        return None

def update_user_calculator(email: str, calculator_config: dict):
    user_doc = get_user_by_email(email)
    if not user_doc:
        raise Exception("User not found")
    user_doc["calculator"] = calculator_config
    _container.upsert_item(user_doc)

def search_universities(query: str, limit: int = 10, offset: int = 0):
    query_lower = query.lower()
    query_str = "SELECT * FROM c WHERE CONTAINS(LOWER(c.name), @query)"
    parameters = [{"name": "@query", "value": query_lower}]
    items = list(_uni_container.query_items(query=query_str, parameters=parameters, enable_cross_partition_query=True))
    return items[offset:offset+limit]
