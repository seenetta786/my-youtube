import os
import sys
import logging
from datetime import datetime, timezone, timedelta

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.whatsapp_messenger import WhatsAppWrapper

# Configure logging for CI
log_handlers = [logging.StreamHandler()]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

def send_payment_reminder():
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    
    logger.info(f"Starting Payment Reminder service at {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC ({now_ist.strftime('%Y-%m-%d %H:%M:%S')} IST)")
    
    try:
        logger.info("Initializing WhatsApp wrapper...")
        wrapper = WhatsAppWrapper()
        
        # RCB 2.0 Group ID
        target_id = "120363419563262981@g.us"
        
        # Beautified Template
        message = (
            "💰 *PAYMENT REMINDER* 💰\n\n"
            "Hello Team! This is a friendly reminder regarding the monthly dues/fees.\n\n"
            "✅ *Status:* Pending\n"
            "📅 *Schedule:* Mon, Wed, Fri\n\n"
            "If you have already processed the payment, please *ignore this message* or share the receipt here. "
            "Thank you for your cooperation! 🙏\n\n"
            "---\n"
            "🤖 _Automated by RCB Service_"
        )
        
        logger.info(f"Sending beautified reminder to {target_id}...")
        result = wrapper.send_message(target_id, message)
        
        if "error" in result:
            logger.error(f"Green API Error: {result['error']}")
        elif result.get("status") == "success" or "id" in result:
            logger.info(f"Reminder sent successfully! Message ID: {result.get('id')}")
        else:
            logger.warning(f"Unexpected API response format: {result}")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    send_payment_reminder()
