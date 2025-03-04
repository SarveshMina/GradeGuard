# blob_storage.py
import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# Get these from environment variables
STORAGE_CONNECTION_STRING = os.environ.get("STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER_NAME", "user-avatars")

# Create the blob service client
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def generate_avatar_upload_url(user_email, filename):
    """
    Generates a SAS URL for direct browser upload to blob storage.
    Returns both the upload URL and the final blob URL.
    """
    # Create a safe blob name using user email as folder
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    blob_name = f"{user_email}/{timestamp}_{safe_filename}"
    
    # Get blob client
    blob_client = container_client.get_blob_client(blob_name)
    
    # Generate SAS token with write permission (for frontend upload)
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=CONTAINER_NAME,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(write=True, create=True),
        expiry=datetime.utcnow() + timedelta(minutes=30)
    )
    
    # Full URL for upload
    upload_url = f"{blob_client.url}?{sas_token}"
    
    # Public URL for access after upload
    public_url = blob_client.url
    
    return {
        "uploadUrl": upload_url,
        "avatarUrl": public_url,
        "blobName": blob_name
    }

def delete_avatar(blob_name):
    """
    Deletes an avatar blob by its full name.
    """
    try:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
        return True
    except Exception as e:
        print(f"Error deleting blob: {e}")
        return False