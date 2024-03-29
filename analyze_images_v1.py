import os
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import storage

credentials = service_account.Credentials.from_service_account_file(
    "polished-studio-402920-41100c8f0b19.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Initialize the Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient(credentials = credentials)

# Initialize the Google Cloud Storage client
storage_client = storage.Client(credentials = credentials)

def analyze_image(image_bucket, image_blob_name):
    # Download the image from Google Cloud Storage
    bucket = storage_client.bucket(image_bucket)
    blob = bucket.blob(image_blob_name)
    image_content = blob.download_as_bytes()

    # Perform image analysis
    image = vision.Image(content=image_content)
    response = vision_client.label_detection(image=image)

    # Extract labels from the response
    labels = [label.description for label in response.label_annotations]

    return labels

if __name__ == "__main__":
    image_bucket = "photo-bucket_polished-studio-402920"  
    image_blob_name = "sheep_cats.png"  

    labels = analyze_image(image_bucket, image_blob_name)
    
    if labels:
        print("Labels detected in the image:")
        for label in labels:
            print(label)
    else:
        print("No labels detected in the image.")