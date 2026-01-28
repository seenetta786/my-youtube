import os
import sys
import logging
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.whatsapp_messenger import WhatsAppWrapper

# Configure logging
log_handlers = [logging.StreamHandler()]

# Only attempt to log to file if NOT in GitHub Actions or if .tmp exists/can be created
if os.environ.get("GITHUB_ACTIONS") != "true":
    log_dir = ".tmp"
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_handlers.append(logging.FileHandler(os.path.join(log_dir, "recurring_poll.log")))
    except Exception:
        pass # Fallback to stream logging only

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

def run_rcb_poll():
    logger.info("Starting recurring RCB 2.0 poll...")
    try:
        wrapper = WhatsAppWrapper()
        # RCB 2.0 Group ID
        target_id = "120363419563262981@g.us"
        question = "Tomorrow's game"
        options = ["Yes", "No"]
        
        result = wrapper.send_poll(target_id, question, options)
        
        if "error" in result:
            logger.error(f"Failed to send poll: {result['error']}")
        else:
            logger.info(f"Poll sent successfully! ID: {result.get('id')}")
            
    except Exception as e:
        logger.error(f"Fatal error in recurring poll: {e}")

if __name__ == "__main__":
    run_rcb_poll()
