# database.py

import os
from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DBNAME = os.environ.get("COSMOS_DBNAME")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER")

# Initialize Cosmos client
_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
_db = _client.get_database_client(COSMOS_DBNAME)
_container = _db.get_container_client(COSMOS_CONTAINER)


def create_user(user_dict: dict):
    """
    Inserts a new user record into the Cosmos DB container.
    """
    _container.create_item(user_dict)


def get_user_by_email(email: str):
    """
    Reads a user document by email (used as the partition key and item ID if you'd like).
    Returns the document or None if not found.
    """
    try:
        user_doc = _container.read_item(item=email, partition_key=email)
        return user_doc
    except:
        return None


def get_user_by_username(username: str):
    """
    Queries the container by 'username' field.
    If found, returns the first matching document, otherwise None.
    """
    query = "SELECT * FROM c WHERE c.username = @username"
    params = [{"name": "@username", "value": username}]
    results = list(_container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
    if results:
        return results[0]
    return None
