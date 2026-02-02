import os
import json
import logging
import re
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Add the project root to sys.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.whatsapp_messenger import WhatsAppWrapper

# Configuration
load_dotenv()
GROUP_ID = "120363419563262981@g.us"
PENDING_FILE = os.path.join(os.path.dirname(__file__), "pending_payments.json")
UPI_ID = "firett786@okicici"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def load_pending():
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r") as f:
            return json.load(f)
    return {"pending_members": [], "last_processed_timestamp": 0}

def save_pending(data):
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(PENDING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def analyze_and_update():
    state = load_pending()
    pending_list = state.get("pending_members", [])
    
    if not pending_list:
        logger.info("No pending payments to track.")
        return

    logger.info(f"Analyzing messages for group {GROUP_ID}...")
    wrapper = WhatsAppWrapper()
    
    # Fetch more messages to be safe, e.g., last 50
    try:
        response = wrapper.client.journals.getChatHistory(chatId=GROUP_ID, count=50)
        if response.code != 200:
            logger.error(f"Failed to fetch history: {response.error}")
            return
        
        messages = response.data
    except Exception as e:
        logger.error(f"Error calling Green API: {e}")
        return

    confirmed_payees = set()
    payment_keywords = ["paid", "sent", "done", "transfer", "screenshot", "receipt", "cleared"]
    
    for msg in messages:
        timestamp = msg.get("timestamp", 0)
        if timestamp <= state.get("last_processed_timestamp", 0):
            continue
            
        text = ""
        msg_type = msg.get("type") or msg.get("typeMessage")
        if msg_type == "textMessage":
            text = msg.get("textMessage", "")
        elif msg_type == "extendedTextMessage":
            text = msg.get("extendedTextMessage", {}).get("text", "")
        
        # Check for images (screenshots)
        is_media = msg_type in ["imageMessage", "fileMessage"]
        
        sender_name = msg.get("senderName", "")
        
        # Basic logic: If sender is in pending list AND (mentions payment OR sends media)
        text_lower = text.lower()
        has_payment_keyword = any(kw in text_lower for kw in payment_keywords)
        
        if (has_payment_keyword or is_media):
            # Try to match sender name with pending list
            for member in pending_list:
                if member.lower() in sender_name.lower() or member.lower() in text_lower:
                    confirmed_payees.add(member)
                    logger.info(f"Detected payment from {member} (Message: '{text[:20]}...', Media: {is_media})")

    # Update state
    if confirmed_payees:
        new_pending = [m for m in pending_list if m not in confirmed_payees]
        state["pending_members"] = new_pending
        logger.info(f"Updated pending list. Removed: {', '.join(confirmed_payees)}")
    
    # Update last processed timestamp to the latest message timestamp
    if messages:
        state["last_processed_timestamp"] = max(m.get("timestamp", 0) for m in messages)
        
    save_pending(state)

def generate_reminder_message():
    state = load_pending()
    pending_list = state.get("pending_members", [])
    
    if not pending_list:
        return (
            "🎉 *ALL PAYMENTS CLEARED!* 🎉\n\n"
            "Thank you everyone for the timely payments. Great teamwork! 🙏\n\n"
            "---\n"
            "🤖 _Automated by RCB Service_"
        )

    pending_str = "\n".join([f"• {m} — ₹1,197" for m in pending_list])
    
    message = (
        "💰 *PAYMENT REMINDER* 💰\n\n"
        "Hello Team! This is a reminder regarding the pending dues.\n\n"
        "👤 *Pending Payments (₹1,197 each):*\n"
        f"{pending_str}\n\n"
        f"*UPI ID: {UPI_ID}* 🏦✨\n\n"
        "If you have already processed the payment, please share the receipt or confirmation here. "
        "Thank you! 🙏\n\n"
        "---\n"
        "🤖 _Automated by RCB Service_"
    )
    return message

def send_reminder():
    analyze_and_update()
    message = generate_reminder_message()
    
    wrapper = WhatsAppWrapper()
    logger.info(f"Sending reminder to {GROUP_ID}...")
    result = wrapper.send_message(GROUP_ID, message)
    
    if "error" in result:
        logger.error(f"Error sending message: {result['error']}")
    else:
        logger.info("Reminder sent successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--analyze", action="store_true", help="Only analyze and update the list")
    parser.add_argument("--send", action="store_true", help="Analyze and send the reminder")
    
    args = parser.parse_args()
    
    if args.analyze:
        analyze_and_update()
    elif args.send:
        send_reminder()
    else:
        # Default behavior: analyze and update
        analyze_and_update()
