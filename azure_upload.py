# azure_upload.py

from azure.storage.blob import BlobServiceClient
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

def upload_to_blob(file, filename: str) -> str:
    """
    Uploads a file-like object to Azure Blob Storage under raw/ folder.
    Returns the public blob URL.
    """

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME", "documents")

    blob_service = BlobServiceClient.from_connection_string(connection_string)
    container = blob_service.get_container_client(container_name)

    # Generate unique filename
    ext = filename.split(".")[-1]
    blob_name = f"raw/{uuid.uuid4()}.{ext}"

    # Upload
    container.upload_blob(name=blob_name, data=file, overwrite=True)

    # Construct public URL
    account_url = blob_service.primary_endpoint
    blob_url = f"{account_url}{container_name}/{blob_name}"

    return blob_url