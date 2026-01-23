import os
import requests
import json
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CLICKUP_API_KEY")
BASE_URL = "https://api.clickup.com/api/v2"

def clickup_request(endpoint, method="GET", data=None, params=None):
    if not API_KEY:
        print("Error: CLICKUP_API_KEY not found in .env")
        sys.exit(1)
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
        if response is not None:
            print(f"Response: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clickup_universal.py <endpoint> <method> [json_data]")
        sys.exit(1)
    
    endpoint = sys.argv[1]
    method = sys.argv[2]
    data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    
    result = clickup_request(endpoint, method, data)
    print(json.dumps(result, indent=2))
