import os
import json
from dotenv import load_dotenv
from whatsapp_api_client_python.API import GreenApi

load_dotenv()

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

def dump_info():
    if not ID_INSTANCE or not API_TOKEN:
        print("Error: GREENAPI credentials not found in .env")
        return
    
    client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)
    
    print("--- Settings ---")
    print(client.account.getSettings().data)
    
    print("\n--- State ---")
    print(client.account.getStateInstance().data)

    print("\n--- Try Fetching Contacts via request ---")
    resp = client.request("GET", f"/waInstance{ID_INSTANCE}/getContacts/{API_TOKEN}")
    if resp.code == 200:
        print(f"Total contacts: {len(resp.data)}")
        for c in resp.data:
            name = c.get("name") or c.get("contactName") or "Unknown"
            if "RCB" in name.upper() or "2.0" in name:
                print(f"MATCH: {name} -> {c.get('id')}")
    else:
        print(f"Failed to get contacts: {resp.code}")

    print("\n--- Try Fetching Chats via request ---")
    resp = client.request("GET", f"/waInstance{ID_INSTANCE}/getChats/{API_TOKEN}")
    if resp.code == 200:
        print(f"Total chats: {len(resp.data)}")
        for c in resp.data:
            name = c.get("name") or "Unknown"
            if "RCB" in name.upper() or "2.0" in name:
                print(f"MATCH: {name} -> {c.get('id')}")
    else:
        print(f"Failed to get chats: {resp.code}")

if __name__ == "__main__":
    dump_info()
