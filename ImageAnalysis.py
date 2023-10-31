import os
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import storage
import google.api_core.exceptions

class ImageAnalysis:
    def __init__(self, bucket_name, credentials_path='polished-studio-402920-41100c8f0b19.json'):
        self.bucket_name = bucket_name
        self.credentials_path = credentials_path
        # stores the vision client for use after initializaion
        self.vision_client = self._initialize_vision_client()
        # stores the storage client for use after initialization
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

    def analyze_image(self, image_blob_name):
        try:
            # Get the bucket using the client
            bucket = self.storage_client.get_bucket(self.bucket_name)  
            # Get the blob within the bucket
            blob = bucket.blob(image_blob_name)
            image_content = blob.download_as_bytes()

            image = vision.Image(content = image_content)
            response = self.vision_client.label_detection(image = image)

            labels = [label.description for label in response.label_annotations]

            return labels

        except google.api_core.exceptions.GoogleAPICallError as e:
            print(f"Google Cloud Vision API Error: {str(e)}")
            return []





