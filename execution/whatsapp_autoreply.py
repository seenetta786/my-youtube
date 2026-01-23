import os
import time
import json
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv
from whatsapp_api_client_python.API import GreenApi

# Get the absolute path of the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

ID_INSTANCE = os.getenv("GREENAPI_ID_INSTANCE")
API_TOKEN = os.getenv("GREENAPI_API_TOKEN")

# Use absolute paths for state and log files
STATE_FILE = os.path.join(BASE_DIR, ".tmp/autoreply_state.json")
LOG_FILE = os.path.join(BASE_DIR, ".tmp/autoreply.log")

# Setup logging
def setup_logging():
    logger = logging.getLogger("whatsapp_autoreply")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
        # File handler
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        fh = logging.FileHandler(LOG_FILE)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Stream handler
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    return logger

logger = setup_logging()

class StateTracker:
    def __init__(self, filepath):
        self.filepath = filepath
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    logger.info(f"Loaded state from {self.filepath}: {len(data)} contacts tracked.")
                    return data
            except Exception as e:
                logger.error(f"Error loading state file {self.filepath}: {e}")
        else:
            logger.info(f"No state file found at {self.filepath}, starting fresh.")
        return {}

    def _save_state(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w") as f:
                json.dump(self.state, f, indent=2)
            logger.info(f"State saved successfully to {self.filepath}")
        except Exception as e:
            logger.error(f"Error saving state file {self.filepath}: {e}")

    def should_reply(self, chat_id):
        today = datetime.now().strftime("%Y-%m-%d")
        last_sent = self.state.get(chat_id)
        if last_sent == today:
            return False
        return True

    def mark_sent(self, chat_id):
        self.state[chat_id] = datetime.now().strftime("%Y-%m-%d")
        self._save_state()

def start_autoreply():
    if not ID_INSTANCE or not API_TOKEN:
        logger.error("GREENAPI credentials missing in .env")
        return

    client = GreenApi(idInstance=ID_INSTANCE, apiTokenInstance=API_TOKEN)
    tracker = StateTracker(STATE_FILE)
    logger.info("WhatsApp Auto-Reply service started. Polling for messages...")

    # The reply message
    AUTO_REPLY_TEXT = "I will attend you soon..."

    consecutive_quota_exceeded_errors = 0
    MAX_CONSECUTIVE_QUOTA_ERRORS = 5
    QUOTA_EXCEEDED_PAUSE_SECONDS = 3600 # Pause for 1 hour

    try:
        while True:
            # Receive notification (polling)
            receive_resp = client.receiving.receiveNotification()
            
            if receive_resp.code == 466:
                consecutive_quota_exceeded_errors += 1
                logger.critical(
                    f"GreenAPI Monthly Quota Exceeded (Status 466). "
                    f"Please upgrade your plan at https://console.green-api.com. "
                    f"Consecutive errors: {consecutive_quota_exceeded_errors}/{MAX_CONSECUTIVE_QUOTA_ERRORS}"
                )
                if consecutive_quota_exceeded_errors >= MAX_CONSECUTIVE_QUOTA_ERRORS:
                    logger.critical(f"Reached {MAX_CONSECUTIVE_QUOTA_ERRORS} consecutive quota errors. Pausing for {QUOTA_EXCEEDED_PAUSE_SECONDS} seconds.")
                    time.sleep(QUOTA_EXCEEDED_PAUSE_SECONDS)
                    consecutive_quota_exceeded_errors = 0 # Reset after a long pause
                time.sleep(5) # Short pause before next attempt if not long paused
                continue # Skip processing this notification and try again
            elif receive_resp.code == 200 and receive_resp.data:
                consecutive_quota_exceeded_errors = 0 # Reset counter on successful response
                receipt_id = receive_resp.data.get("receiptId")
                body = receive_resp.data.get("body", {})
                type_webhook = body.get("typeWebhook")
                chat_id = body.get("senderData", {}).get("chatId")

                # Handle incoming messages only
                if type_webhook == "incomingMessageReceived" and chat_id:
                    sender_name = body.get("senderData", {}).get("senderName", "Unknown")
                    
                    if tracker.should_reply(chat_id):
                        logger.info(f"New message from {sender_name} ({chat_id}). Sending auto-reply...")
                        
                        # Send auto-reply
                        send_resp = client.sending.sendMessage(chatId=chat_id, message=AUTO_REPLY_TEXT)
                        
                        if send_resp.code == 466:
                            consecutive_quota_exceeded_errors += 1
                            logger.critical(
                                f"GreenAPI Monthly Quota Exceeded (Status 466) when sending message to {chat_id}. "
                                f"Please upgrade your plan at https://console.green-api.com. "
                                f"Consecutive errors: {consecutive_quota_exceeded_errors}/{MAX_CONSECUTIVE_QUOTA_ERRORS}"
                            )
                            if consecutive_quota_exceeded_errors >= MAX_CONSECUTIVE_QUOTA_ERRORS:
                                logger.critical(f"Reached {MAX_CONSECUTIVE_QUOTA_ERRORS} consecutive quota errors. Pausing for {QUOTA_EXCEEDED_PAUSE_SECONDS} seconds.")
                                time.sleep(QUOTA_EXCEEDED_PAUSE_SECONDS)
                                consecutive_quota_exceeded_errors = 0 # Reset after a long pause
                        elif send_resp.code == 200:
                            consecutive_quota_exceeded_errors = 0 # Reset counter on successful send
                            logger.info(f"Auto-reply sent successfully to {chat_id}")
                            tracker.mark_sent(chat_id)
                        else:
                            logger.error(f"Failed to send auto-reply: {send_resp.code} {send_resp.data}")
                    else:
                        logger.info(f"Message from {sender_name} ({chat_id}) ignored. Auto-reply already sent today.")

                # Always delete the notification to acknowledge it
                if receipt_id:
                    client.receiving.deleteNotification(receiptId=receipt_id)
            
            # Small sleep to be polite to the API
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Auto-Reply service stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error in Auto-Reply service: {e}")

if __name__ == "__main__":
    start_autoreply()
