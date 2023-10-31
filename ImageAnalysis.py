import os
import json 
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import storage
import google.api_core.exceptions

class ImageAnalysis:
    # constructor: 
    def __init__(self, bucket_name, credentials_path='polished-studio-402920-41100c8f0b19.json'):
        self.bucket_name = bucket_name
        self.credentials_path = credentials_path
        # stores the vision client for use in instance
        self.vision_client = self._initialize_vision_client()
        # stores the storage client for use in instance
        self.storage_client = self._initialize_storage_client()

    def _initialize_vision_client(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        vision_client = vision.ImageAnnotatorClient(credentials = credentials)

        return vision_client

    def _initialize_storage_client(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        storage_client = storage.Client(credentials = credentials)

        return storage_client

    def is_image_blob(self, blob):
        valid_image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
        # Get the file extension from the blob's name
        file_extension = os.path.splitext(blob.name)[1].lower()
        
        return file_extension in valid_image_extensions

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

    def bulk_analyze_images_to_console(self, bucket_path):
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            subdirectory_path = bucket_path

            for blob in bucket.list_blobs():
                if blob.name.startswith(subdirectory_path) and self.is_image_blob(blob):
                    print(f"File name: {blob.name}")
                    labels = self.analyze_image(blob.name)
                    if labels:
                        print("Labels detected:")
                        for label in labels:
                            print(label)
                    else:
                        print("No labels detected")
                    print()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def bulk_analyze_images_to_json(self, bucket_path, file_name):
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            subdirectory_path = bucket_path
            data_list = []

            for blob in bucket.list_blobs():
                if blob.name.startswith(subdirectory_path) and self.is_image_blob(blob):
                    print(f"File name: {blob.name}")
                    labels = self.analyze_image(blob.name)
                    filename = blob.name.split("/")[-1] # Extract just the filename
                    if labels:
                        new_data = { 
                            "Filename": filename, 
                            "Labels": labels  
                        }        
                    else: 
                        new_data = { 
                            "Filename": filename, 
                            "Labels": "no labels detected." 
                        }        
                    data_list.append(new_data)

            with open(file_name, "w") as json_file:
                json.dump(data_list, json_file, indent = 4)       
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")


         

  





