import os
from google.oauth2 import service_account
from google.cloud import storage

credentials = service_account.Credentials.from_service_account_file(
    "polished-studio-402920-41100c8f0b19.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Initialize the Google Cloud Storage client
storage_client = storage.Client(credentials = credentials)

local_dir = "/Users/robertwatson/Desktop/things_from_desktop"

def upload_images_to_gcs(bucket_name, local_directory, destination_path):
    # Get the bucket 
    bucket = storage_client.get_bucket(bucket_name)

    # only include jpgs 
    local_files = [ f for f in os.listdir(local_directory) 
    if os.path.isfile( os.path.join(local_directory, f) ) and f.endswith('.jpg') ]

    for local_file in local_files:
        source_file_path = os.path.join(local_directory, local_file)
        destination_blob_name = os.path.join(destination_path, local_file)

        # Create a blob with the destination path
        blob = bucket.blob(destination_blob_name) 
        # Upload the local file to the blob 
        blob.upload_from_filename(source_file_path)  
    
if __name__ == '__main__':
    bucket_name = 'photo-bucket_polished-studio-402920'  
    local_directory = '/Users/robertwatson/Desktop/things_from_desktop'  
    destination_path = 'imgs_for_tagging/'

    upload_images_to_gcs(bucket_name, local_directory, destination_path)