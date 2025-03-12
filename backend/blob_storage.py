# blob_storage.py
import os
import logging
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import AzureError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get these from environment variables
STORAGE_CONNECTION_STRING = os.environ.get("STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER_NAME", "user-avatars")

def generate_avatar_upload_url(user_email, filename):
    """
    Generates a SAS URL for direct browser upload to blob storage.
    Returns both the upload URL and the final blob URL.
    """
    try:
        # Validate inputs
        if not user_email:
            raise ValueError("User email is required")
        if not filename:
            raise ValueError("Filename is required")

        # Validate storage connection
        if not STORAGE_CONNECTION_STRING:
            raise ValueError("Storage connection string is not configured")

        # Create blob service client
        try:
            blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        except Exception as e:
            logger.error(f"Failed to create blob service client: {str(e)}")
            raise

        # Create a safe blob name using user email as folder
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        blob_name = f"{user_email}/{timestamp}_{safe_filename}"
        
        # Get blob client
        blob_client = container_client.get_blob_client(blob_name)
        
        # Generate SAS token with write permission (for frontend upload)
        try:
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=CONTAINER_NAME,
                blob_name=blob_name,
                account_key=blob_service_client.credential.account_key,
                permission=BlobSasPermissions(write=True, create=True),
                expiry=datetime.utcnow() + timedelta(minutes=30)
            )
        except Exception as e:
            logger.error(f"Failed to generate SAS token: {str(e)}")
            raise
        
        # Full URL for upload
        upload_url = f"{blob_client.url}?{sas_token}"
        
        # Public URL for access after upload
        public_url = blob_client.url
        
        logger.info(f"Generated upload URL for {user_email}: {upload_url}")
        logger.info(f"Public avatar URL: {public_url}")
        
        return {
            "uploadUrl": upload_url,
            "avatarUrl": public_url,
            "blobName": blob_name
        }
    except Exception as e:
        logger.error(f"Error in generate_avatar_upload_url: {str(e)}")
        raise

def delete_avatar(blob_name):
    """
    Deletes an avatar blob by its full name.
    """
    try:
        # Validate inputs
        if not blob_name:
            raise ValueError("Blob name is required")

        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
        
        logger.info(f"Successfully deleted blob: {blob_name}")
        return True
    except AzureError as e:
        logger.error(f"Azure error deleting blob {blob_name}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error deleting blob {blob_name}: {str(e)}")
        return False