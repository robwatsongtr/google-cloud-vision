import os
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import storage
import google.api_core.exceptions

credentials = service_account.Credentials.from_service_account_file(
    "polished-studio-402920-41100c8f0b19.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Initialize the Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient(credentials = credentials)

# Initialize the Google Cloud Storage client
storage_client = storage.Client(credentials = credentials)

# check if blob is a valid image file. Returns boolean. 
def is_image_blob(blob):
    valid_image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    # Get the file extension from the blob's name
    file_extension = os.path.splitext(blob.name)[1].lower()
    return file_extension in valid_image_extensions

def analyze_image(bucket, image_blob_name):
    try:
        blob = bucket.blob(image_blob_name)
        image_content = blob.download_as_bytes()

        # Perform image analysis
        image = vision.Image(content=image_content)
        response = vision_client.label_detection(image=image)

        # Extract labels from the response
        labels = [label.description for label in response.label_annotations]

        return labels

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Vision API Error: {str(e)}")
        return []
    

def bulk_analyze_images(bucket_name, bucket_path):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        subdirectory_path = bucket_path

        for blob in bucket.list_blobs():
            if blob.name.startswith(subdirectory_path) and is_image_blob(blob):
                print(f"File name: {blob.name}")
                labels = analyze_image(bucket, blob.name)
                if labels:
                    print("Labels detected:")
                    for label in labels:
                        print(label)
                else:
                    print("No labels detected")
                print()

    except Exception as e:
        # Handle exceptions here, e.g., log the error or return an error message
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    bucket_name = 'photo-bucket_polished-studio-402920'
    bucket_path = 'imgs_for_tagging/'

    bulk_analyze_images(bucket_name, bucket_path)

