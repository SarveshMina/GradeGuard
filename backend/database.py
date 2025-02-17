import os
from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DBNAME = os.environ.get("COSMOS_DBNAME")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER")  # user container

# NEW environment variable or config for the "universities" container name
COSMOS_UNI_CONTAINER = os.environ.get("COSMOS_UNI_CONTAINER")  # e.g. "universities"

# Initialize Cosmos client
_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
_db = _client.get_database_client(COSMOS_DBNAME)

# User container
_container = _db.get_container_client(COSMOS_CONTAINER)

# University container
_uni_container = _db.get_container_client(COSMOS_UNI_CONTAINER)


def create_user(user_dict: dict):
    """
    Inserts a new user record into the Cosmos DB container.
    """
    _container.create_item(user_dict)


def get_user_by_email(email: str):
    """
    Reads a user document by email. Returns the document or None if not found.
    """
    try:
        user_doc = _container.read_item(item=email, partition_key=email)
        return user_doc
    except Exception:
        return None


def increment_university_and_major_counter(university_name: str, major_name: str):
    """
    Reads/creates the document for the given university, increments its 'counter',
    and also increments the 'counter' for the specific major within 'majors'.
    Then upserts the document back into the universities container.
    """
    try:
        # Attempt to read the existing document using the university name as the partition key.
        uni_doc = _uni_container.read_item(item=university_name, partition_key=university_name)
    except:
        # If the document does not exist, create a new one
        uni_doc = {
            "id": university_name,
            "name": university_name,  # partition key
            "counter": 0,
            "majors": []
        }

    # Increment the total counter for this university
    uni_doc["counter"] = uni_doc.get("counter", 0) + 1

    # Find the major in the 'majors' array
    major_found = None
    for m in uni_doc["majors"]:
        if m["major_name"].lower() == major_name.lower():
            major_found = m
            break

    # If the major is found, increment its counter; otherwise add a new entry
    if major_found:
        major_found["counter"] += 1
    else:
        uni_doc["majors"].append({
            "major_name": major_name,
            "counter": 1
        })

    # Finally, upsert the document back to Cosmos
    _uni_container.upsert_item(uni_doc)


def get_all_universities_docs():
    """
    Returns a list of all documents in the universities container.
    """
    query = "SELECT * FROM c"
    items = list(_uni_container.query_items(query=query, enable_cross_partition_query=True))
    return items


def get_university_doc(university_name: str):
    """
    Reads a single university doc by name (partition key).
    Returns None if not found.
    """
    try:
        doc = _uni_container.read_item(item=university_name, partition_key=university_name)
        return doc
    except:
        return None
