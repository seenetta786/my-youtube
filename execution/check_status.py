import os
import sys

# Minimalist check script
from whatsapp_api_client_python.API import GreenApi

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

def check_status():
    if not ID_INSTANCE or not API_TOKEN:
        print("Credentials missing in environment")
        return

    print(f"Checking Instance: {ID_INSTANCE}")
    client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)
    try:
        response = client.serviceMethods.getStateInstance()
        print(f"Instance State: {response.data}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_status()
