# utils/azure_blob_utils.py

from azure.storage.blob import BlobServiceClient
import logging
from config.config import AZURE_BLOB_CONFIG

def downloadBlobFromAzure(blobName, storageFolder, downloadName):
    finalSavingPath = "assets/" + storageFolder + "/" + downloadName
    account_name = AZURE_BLOB_CONFIG['account_name']
    account_key = AZURE_BLOB_CONFIG['account_key']
    container_name = AZURE_BLOB_CONFIG['container_name']
    try:
        blobServiceClient = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key
        )
        container_client = blobServiceClient.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blobName)

        with open(finalSavingPath, "wb") as download_file:
            download_stream = blob_client.download_blob()
            download_file.write(download_stream.readall())
        logging.info(f"Blob {blobName} downloaded to {finalSavingPath}")
        print(f"Blob {blobName} downloaded to {finalSavingPath}")
    except Exception as e:
        logging.error(f"Error downloading blob: {e}")
