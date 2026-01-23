import os
import json
from dotenv import load_dotenv
from whatsapp_api_client_python.API import GreenApi

load_dotenv()

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

def find_contact(name_query):
    if not ID_INSTANCE or not API_TOKEN:
        print("Error: GREENAPI credentials not found in .env")
        return None
    
    client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)
    
    print(f"Searching for contact matching: {name_query}")
    try:
        response = client.serviceMethods.getContacts()
        if response.code == 200:
            contacts = response.data
            for contact in contacts:
                name = contact.get("name") or contact.get("contactName") or ""
                if name_query.lower() in name.lower():
                    return contact
        else:
            print(f"Error fetching contacts: {response.code} {response.error}")
    except Exception as e:
        print(f"Exception during getContacts: {e}")

    return None

if __name__ == "__main__":
    contact = find_contact("RCB 2.0")
    if contact:
        print(f"Found contact:\n{json.dumps(contact, indent=2)}")
    else:
        print("Contact not found.")
