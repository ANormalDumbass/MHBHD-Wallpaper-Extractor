import os
import requests
import time

# Directory to save images (Ex: C:/Users/redacted/Downloads/wallpaper_data)
base_dir = "downloaded_images"
# Time to wait between requests (in seconds)
request_delay = 1  # Adjust the delay as needed
# JSON Data gathered from an URL (The Database to the Images)
json_url = 'https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s'

def download_image(url, save_path):
    """Downloads an image from the extrated JSON data, then saves it onto a folder"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the download fails
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def process_json_data(json_data):
    """Processes the JSON data and downloads the images."""
    for key, value in json_data['data'].items():
        # Create a folder for the current key
        folder_path = os.path.join(base_dir, key)
        os.makedirs(folder_path, exist_ok=True)
        
        # Iterate over all items within each key
        for sub_key, url in value.items():
            # Check if the value is a valid URL (starts with 'http')
            if isinstance(url, str) and url.startswith('http'):
                # Generate a filename for the image based on the sub_key (e.g., "s_image.jpg")
                image_filename = f"{sub_key}_image.jpg"
                image_save_path = os.path.join(folder_path, image_filename)
                
                # Download the image
                download_image(url, image_save_path)
                
                # Pause between requests to avoid overloading the server
                time.sleep(request_delay)

def fetch_json_from_url(url):
    """Fetches JSON data from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON data from {url}: {e}")
        return None

# Fetch the JSON data from the provided URL
json_data = fetch_json_from_url(json_url)

if json_data:
    # Ensure base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Process the JSON content and download images
    process_json_data(json_data)
