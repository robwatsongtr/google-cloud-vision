import os
import json 
import xml.etree.ElementTree as ET
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import storage
import google.api_core.exceptions
import xml.dom.minidom

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

    def flatten_data(self, d):
        flattened = {}

        # recursively flatten any nested dics or lists 
        def flatten(x, name=""):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + "_")
            elif type(x) is list:
                for i, a in enumerate(x):
                    flatten(a, name + str(i) + "_")
            else:
                flattened[name[:-1]] = x

        flatten(d)
        return flattened

    def get_labels_from_images(self, bucket_path, file_name):
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

            return data_list
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def bulk_analyze_images_to_json(self, bucket_path, file_name):
        try:
            images_labels = self.get_labels_from_images(bucket_path, file_name)

            with open(file_name, "w") as json_file:
                json.dump(images_labels, json_file, indent = 4)       
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def bulk_analyze_images_to_XML(self, bucket_path, file_name):
        try:
            images_labels = self.get_labels_from_images(bucket_path, file_name)
            
            # Flatten out the nested lists of labels 
            flattened_struct = [ self.flatten_data(item) for item in images_labels ]

            # define root of XML tree 
            root = ET.Element("data")

            # iterate and build XML tree
            for data_dict in flattened_struct:
                dict_element = ET.SubElement(root, "Image")
                for key, value in data_dict.items():
                    item_element = ET.SubElement(dict_element, key)
                    item_element.text = value

            tree = ET.ElementTree(root)

            # Serialize the XML data and format it for readability
            xml_str = ET.tostring(root, encoding="unicode")
            pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml()

            # Write the formatted XML to a file
            with open(file_name, "w") as xml_file:
                xml_file.write(pretty_xml)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")



        




