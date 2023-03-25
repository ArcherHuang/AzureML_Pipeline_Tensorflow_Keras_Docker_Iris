import os
from dotenv import load_dotenv
from azure.storage.blob import BlobClient, BlobServiceClient

load_dotenv()
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

# 列出所有 Blob 並刪除
blobs = container_client.list_blobs()
for index, blob in enumerate(blobs):
    print(f"[{index+1}] File: {blob.name}")
    to_delete_file = blob_service_client.get_blob_client(
        container=BLOB_CONTAINER_NAME,
        blob=blob.name
    )
    to_delete_file.delete_blob()
