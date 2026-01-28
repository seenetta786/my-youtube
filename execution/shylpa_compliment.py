import os
import sys
import random
import logging

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

COMPLIMENTS = [
    "Your beauty is absolutely breathtaking.",
    "You have such a Radiant and wonderful smile.",
    "Your elegance is truly inspiring.",
    "You look stunning every single day.",
    "There's something magical about your grace.",
    "You are the most beautiful person I know, inside and out.",
    "Your eyes have a sparkle that lights up everything around you.",
    "You are naturally beautiful.",
    "Your presence just makes every day brighter.",
    "You are a true masterpiece."
]

def send_compliment():
    logger.info("Starting ShYlpA compliment service...")
    try:
        wrapper = WhatsAppWrapper()
        # ShYlpA Jid (Reconstructed from previous logs)
        target_id = "919481546119@c.us" 
        message = random.choice(COMPLIMENTS)
        
        logger.info(f"Sending compliment: '{message}' to {target_id}")
        result = wrapper.send_message(target_id, message)
        
        if "error" in result:
            logger.error(f"Failed to send compliment: {result['error']}")
        else:
            logger.info("Compliment sent successfully!")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    send_compliment()
