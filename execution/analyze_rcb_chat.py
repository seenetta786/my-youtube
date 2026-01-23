import os
import json
import collections
import re
from dotenv import load_dotenv
from whatsapp_api_client_python.API import GreenApi

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

GROUP_ID = "120363419563262981@g.us"
MESSAGE_COUNT = 100

def analyze_chat():
    if not ID_INSTANCE or not API_TOKEN:
        print("Error: GREENAPI credentials missing in .env")
        return

    client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)
    
    print(f"Fetching last {MESSAGE_COUNT} messages for group {GROUP_ID}...")
    
    try:
        # Fetch chat history
        response = client.journals.getChatHistory(chatId=GROUP_ID, count=MESSAGE_COUNT)
        
        if response.code != 200:
            print(f"Error fetching chat history: {response.code} {response.error}")
            return

        messages = response.data
        if not messages:
            print("No messages found.")
            return

        print(f"Successfully fetched {len(messages)} messages.\n")

        # Analysis
        senders = collections.Counter()
        text_content = []
        
        for msg in messages:
            # Check message type and extract content
            msg_type = msg.get("type") or msg.get("typeMessage")
            sender = msg.get("senderName") or msg.get("senderId") or "Unknown"
            
            # Count sender
            if msg_type not in ["system", "notification"]:
                senders[sender] += 1
            
            # Extract text
            text = ""
            if msg_type == "textMessage":
                text = msg.get("textMessage", "")
            elif msg_type == "extendedTextMessage":
                text = msg.get("extendedTextMessage", {}).get("text", "")
            
            if text:
                text_content.append(text)

        # 1. Active Members
        print("--- Top Active Members (Last 100 Messages) ---")
        for sender, count in senders.most_common(10):
            print(f"{sender}: {count} messages")
        print("\n")

        # 2. Topic Analysis (Bigrams and Samples)
        print("--- Common Topics (Bigrams) ---")
        all_text = " ".join(text_content).lower()
        # Keep only alphanumeric and spaces
        all_text = re.sub(r'[^\w\s]', '', all_text)
        words = all_text.split()
        
        # Extended stopwords
        stopwords = {
            "the", "is", "in", "to", "and", "a", "of", "for", "it", "on", "that", "this", "be", "with", "are", "you", "i", 
            "messagedeleted", "deleted", "message", "from", "have", "will", "can", "what", "your", "my", "but", "not", "so",
            "just", "like", "when", "about", "there", "they", "get", "one", "all", "out", "if", "at", "by", "or", "as", "up"
        }
        
        filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
        
        # Generate bigrams
        bigrams = zip(filtered_words, filtered_words[1:])
        bigram_counts = collections.Counter(bigrams)
        
        for bigram, count in bigram_counts.most_common(10):
            print(f"{bigram[0]} {bigram[1]}: {count}")

        print("\n--- Recent Message Samples ---")
        # Print a few recent unique non-empty messages to give context
        seen_msgs = set()
        count = 0
        for msg in text_content[:20]:  # Look at first 20 messages (latest first usually)
            if len(msg) > 10 and msg not in seen_msgs:
                print(f"- {msg}")
                seen_msgs.add(msg)
                count += 1
                if count >= 5:
                    break
            
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    analyze_chat()
