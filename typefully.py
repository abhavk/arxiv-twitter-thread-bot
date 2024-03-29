import os
import requests
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

base_url = "https://api.typefully.com/v1"
api_key = os.environ.get("TYPEFULLY_API_KEY")

def create_tweet(text):
    url = f"{base_url}/drafts/"
    headers = {
        "X-API-KEY": api_key
    }

    data = {
        "content": text,
        "threadify": True,
        "share": True
    }

    response = requests.post(url, headers=headers, json=data) 
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create a tweet. Error: {response.text}")
