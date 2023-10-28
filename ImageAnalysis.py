import os
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import storage
import google.api_core.exceptions

class ImageAnalysis:
    def __init__(self, project_id, bucket_name, credentials_path='polished-studio-402920-41100c8f0b19.json'):
        """
        Initialize the ImageAnalysis instance.

        Args:
            project_id (str): The Google Cloud Project ID.
            bucket_name (str): The name of the Google Cloud Storage bucket containing images.
            credentials_path (str, optional): Path to the JSON key file for service account authentication.
        """
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.credentials_path = credentials_path
        self.vision_client = self._initialize_vision_client()
        self.storage_client = self._initialize_storage_client()


    def _initialize_vision_client(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)

        # Initialize the Google Cloud Vision client
        vision_client = vision.ImageAnnotatorClient(credentials = credentials)

        return vision_client

    def _initialize_storage_client(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client(credentials = credentials)

        return storage_client
