import os
import json
import argparse
from dotenv import load_dotenv
from whatsapp_api_client_python.API import GreenApi

load_dotenv()

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

class WhatsAppWrapper:
    def __init__(self):
        if not ID_INSTANCE or not API_TOKEN:
            raise ValueError("GREENAPI credentials missing in .env")
        self.client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)

    def find_chat(self, name_query):
        # Search in contacts
        try:
            response = self.client.serviceMethods.getContacts()
            if response.code == 200:
                for contact in response.data:
                    name = contact.get("name") or contact.get("contactName") or ""
                    if name_query.lower() in name.lower():
                        return contact.get("id")
        except Exception as e:
            print(f"Error searching contacts: {e}")
        
        return None

    def send_message(self, target, message):
        chat_id = target
        if "@" not in target:
            # Assume it's a name, try to find ID
            chat_id = self.find_chat(target)
            if not chat_id:
                return {"error": f"Contact '{target}' not found"}
        
        response = self.client.sending.sendMessage(chatId=chat_id, message=message)
        if response.code == 200:
            return {"status": "success", "id": response.data.get("idMessage")}
        else:
            return {"error": response.data if response.data else f"Status code {response.code}"}

    def send_poll(self, target, question, options):
        chat_id = target
        if "@" not in target:
            chat_id = self.find_chat(target)
            if not chat_id:
                return {"error": f"Contact '{target}' not found"}
        
        formatted_options = [{"optionName": opt} for opt in options]
        response = self.client.sending.sendPoll(chatId=chat_id, message=question, options=formatted_options)
        if response.code == 200:
            return {"status": "success", "id": response.data.get("idMessage")}
        else:
            return {"error": response.data if response.data else f"Status code {response.code}"}

def main():
    parser = argparse.ArgumentParser(description="WhatsApp Messenger Wrapper")
    parser.add_argument("--to", help="Contact name or ID")
    parser.add_argument("--msg", help="Message content")
    parser.add_argument("--get-contacts", action="store_true", help="List all contacts")
    parser.add_argument("--get-chats", action="store_true", help="List all chats")
    parser.add_argument("--poll-question", help="Poll question")
    parser.add_argument("--poll-options", nargs="+", help="Poll options (space separated)")
    
    args = parser.parse_args()
    wrapper = WhatsAppWrapper()

    if args.get_contacts:
        response = wrapper.client.serviceMethods.getContacts()
        if response.code == 200:
            contacts = response.data
            # Sort contacts by name, handle None/empty cases
            sorted_contacts = sorted(
                contacts, 
                key=lambda x: (x.get("name") or x.get("contactName") or x.get("id") or "").lower()
            )
            print(json.dumps(sorted_contacts, indent=2))
        else:
            print(json.dumps({"error": response.error}, indent=2))
    elif args.get_chats:
        # GreenAPI Journals for chats
        chats = wrapper.client.request("GET", "getChats")
        print(json.dumps(chats.data, indent=2))
    elif args.to and args.poll_question and args.poll_options:
        result = wrapper.send_poll(args.to, args.poll_question, args.poll_options)
        print(json.dumps(result, indent=2))
    elif args.to and args.msg:
        result = wrapper.send_message(args.to, args.msg)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
