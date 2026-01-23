import os
import json
import sys
from dotenv import load_dotenv
from whatsapp_api_client_python.API import GreenApi

load_dotenv()

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

def send_to_rcb():
    if not ID_INSTANCE or not API_TOKEN:
        print("Error: GREENAPI credentials not found in .env")
        return
    
    client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)
    group_id = "120363419563262981@g.us"
    message = "Hello!"
    
    print(f"Sending '{message}' to {group_id} (RCB 2.0)")
    response = client.sending.sendMessage(chatId=group_id, message=message)
    
    if response.code == 200:
        print(f"Success! Message ID: {response.data.get('idMessage')}")
        return True
    else:
        print(f"Failed: {response.code} {response.data}")
        return False

if __name__ == "__main__":
    send_to_rcb()
