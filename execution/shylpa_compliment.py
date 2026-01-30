import os
import sys
# Triggered test run: 2026-01-29 07:31 IST
import random
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

COMPLIMENTS = [
    "Your beauty is absolutely breathtaking.", "You have such a radiant and wonderful smile.",
    "Your elegance is truly inspiring.", "You look stunning every single day.",
    "There's something magical about your grace.", "You are the most beautiful person I know, inside and out.",
    "Your eyes have a sparkle that lights up everything around you.", "You are naturally beautiful.",
    "Your presence just makes every day brighter.", "You are a true masterpiece.",
    "Your kindness adds to your incredible beauty.", "You have such a charming personality.",
    "Your laughter is the most beautiful sound.", "You are a vision of elegance.",
    "Every time I see you, you look even more beautiful.", "Your style is as beautiful as your soul.",
    "You have a heart of gold that shines through your eyes.", "Your confidence is honestly so attractive.",
    "You are mesmerizing in every way.", "Your intelligence is just as beautiful as your face.",
    "You possess a timeless beauty.", "Your inner glow is truly captivating.",
    "You are a breath of fresh air.", "Your smile can brighten the darkest day.",
    "You have such a calming and beautiful presence.", "You are truly one of a kind.",
    "Everything about you is simply lovely.", "Your spirit is incredibly beautiful.",
    "You are more beautiful than words can describe.", "Your beauty is poetic.",
    "You have a radiant energy that is so beautiful.", "You are the definition of grace.",
    "Your beauty shines from within.", "You are simply stunning.",
    "You have the most beautiful soul.", "Every little thing about you is beautiful.",
    "You are an absolute vision.", "You have a natural charm that is so beautiful.",
    "Your beauty is truly captivating.", "You are the most amazing person.",
    "Your warmth is so beautiful.", "You are a light in this world.",
    "You have such a beautiful perspective on life.", "Your strength is incredibly beautiful.",
    "You are a beautiful human being.", "You are glowing today.",
    "Your beauty is understated and elegant.", "You are simply wonderful.",
    "You have a beautiful way with words.", "Your compassion is so beautiful.",
    "You are a beautiful mystery.", "Your adventurous spirit is beautiful.",
    "You are a beautiful inspiration.", "You have a beautiful sense of humor.",
    "Your creative mind is beautiful.", "You are a beautiful dreamer.",
    "Your ambition is beautiful.", "You are a beautiful soul mate.",
    "Your loyalty is beautiful.", "You are a beautiful friend.",
    "Your honesty is beautiful.", "You are a beautiful listener.",
    "Your patience is beautiful.", "You are a beautiful healer.",
    "Your wisdom is beautiful.", "You are a beautiful warrior.",
    "Your vulnerability is beautiful.", "You are a beautiful star.",
    "Your shine is beautiful.", "You are a beautiful flower.",
    "Your bloom is beautiful.", "You are a beautiful sunset.",
    "Your colors are beautiful.", "You are a beautiful ocean.",
    "Your depth is beautiful.", "You are a beautiful mountain.",
    "Your peak is beautiful.", "You are a beautiful forest.",
    "Your life is beautiful.", "You are a beautiful melody.",
    "Your rhythm is beautiful.", "You are a beautiful dance.",
    "Your movement is beautiful.", "You are a beautiful story.",
    "Your chapters are beautiful.", "You are a beautiful poem.",
    "Your verses are beautiful.", "You are a beautiful song.",
    "Your lyrics are beautiful.", "You are a beautiful diamond.",
    "Your facets are beautiful.", "You are a beautiful pearl.",
    "Your luster is beautiful.", "You are a beautiful painting.",
    "Your strokes are beautiful.", "You are a beautiful sculpture.",
    "Your shape is beautiful.", "You are a beautiful design.",
    "Your pattern is beautiful.", "You are a beautiful light.",
    "Your ray is beautiful.", "You are a beautiful fire.",
    "Your flame is beautiful.", "You are a beautiful cloud.",
    "Your soft edges are beautiful.", "You are a beautiful breeze.",
    "Your touch is beautiful.", "You are a beautiful rain.",
    "Your sound is beautiful.", "You are a beautiful snow.",
    "Your flake is beautiful.", "You are a beautiful season.",
    "Your change is beautiful.", "You are a beautiful moment.",
    "Your stillness is beautiful.", "You are a beautiful memory.",
    "Your trace is beautiful.", "You are a beautiful hope.",
    "Your wish is beautiful.", "You are a beautiful dream.",
    "Your sleep is beautiful.", "You are a beautiful wake.",
    "Your morning is beautiful.", "You are a beautiful noon.",
    "Your evening is beautiful.", "You are a beautiful night.",
    "Your moon is beautiful.", "You are a beautiful star.",
    "Your constellation is beautiful.", "You are a beautiful galaxy.",
    "Your space is beautiful.", "You are a beautiful planet.",
    "Your world is beautiful.", "You are a beautiful atmosphere.",
    "Your air is beautiful.", "You are a beautiful gravity.",
    "Your pull is beautiful.", "You are a beautiful energy.",
    "Your vibration is beautiful.", "You are a beautiful frequency.",
    "Your signal is beautiful.", "You are a beautiful echo.",
    "Your bounce is beautiful.", "You are a beautiful mirror.",
    "Your reflection is beautiful.", "You are a beautiful shadow.",
    "Your dark is beautiful.", "You are a beautiful light.",
    "Your bright is beautiful.", "You are a beautiful contrast.",
    "Your balance is beautiful.", "You are a beautiful harmony.",
    "Your tune is beautiful.", "You are a beautiful beat.",
    "Your pulse is beautiful.", "You are a beautiful heart.",
    "Your beat is beautiful.", "You are a beautiful breath.",
    "Your life is beautiful.", "You are a beautiful step.",
    "Your path is beautiful.", "You are a beautiful journey.",
    "Your destination is beautiful.", "You are a beautiful arrival.",
    "Your welcome is beautiful.", "You are a beautiful stay.",
    "Your comfort is beautiful.", "You are a beautiful home.",
    "Your warmth is beautiful.", "You are a beautiful safety.",
    "Your shield is beautiful.", "You are a beautiful sword.",
    "Your fight is beautiful.", "You are a beautiful peace.",
    "Your calm is beautiful.", "Your quiet is beautiful.",
    "Your loud is beautiful.", "Your voice is beautiful.",
    "Your silence is beautiful.", "Your thought is beautiful.",
    "Your idea is beautiful.", "Your vision is beautiful.",
    "Your goal is beautiful.", "Your win is beautiful.",
    "Your fail is beautiful.", "Your try is beautiful.",
    "Your work is beautiful.", "Your play is beautiful.",
    "Your laugh is beautiful.", "Your cry is beautiful.",
    "Your smile is beautiful.", "Your frown is beautiful.",
    "Your anger is beautiful.", "Your love is beautiful.",
    "Your hate is beautiful.", "Your care is beautiful.",
    "Your touch is beautiful.", "Your feel is beautiful.",
    "Your look is beautiful.", "Your taste is beautiful.",
    "Your smell is beautiful.", "Your sense is beautiful.",
    "Your mind is beautiful.", "Your soul is beautiful.",
    "Your body is beautiful.", "Your being is beautiful.",
    "Your presence is beautiful.", "Your essence is beautiful.",
    "Your style is beautiful.", "Your grace is beautiful.",
    "Your poise is beautiful.", "Your manners are beautiful.",
    "Your class is beautiful.", "Your power is beautiful.",
    "Your gentleness is beautiful.", "Your kindness is beautiful.",
    "Your mercy is beautiful.", "Your justice is beautiful.",
    "Your truth is beautiful.", "Your lie is beautiful.",
    "Your secret is beautiful.", "Your open is beautiful.",
    "Your hidden is beautiful.", "Your found is beautiful.",
    "Your lost is beautiful.", "Your path is beautiful.",
    "Your road is beautiful.", "Your way is beautiful.",
    "Your light is beautiful.", "Your dark is beautiful.",
    "Your fast is beautiful.", "Your slow is beautiful.",
    "Your stop is beautiful.", "Your go is beautiful.",
    "Your start is beautiful.", "Your end is beautiful.",
    "Your birth is beautiful.", "Your death is beautiful.",
    "Your life is beautiful.", "Your everything is beautiful.",
    "You are the sun on a rainy day.", "You are the moon in a dark night.",
    "You are the stars in a clear sky.", "You are the water in a desert.",
    "You are the food for a hungry soul.", "You are the drink for a thirsty spirit.",
    "You are the rest for a weary traveler.", "You are the hope for a broken heart.",
    "You are the love for a lonely soul.", "You are the joy for a sad heart.",
    "You are the peace for a troubled mind.", "You are the strength for a weak body.",
    "You are the light for a blind eye.", "You are the sound for a deaf ear.",
    "You are the feel for a numb hand.", "You are the smell for a blocked nose.",
    "You are the taste for a dull tongue.", "You are the sense for a lost mind.",
    "You are the soul for a dead body.", "You are the life for a dead world.",
    "You are the universe in a single person.", "You are the galaxy in a single eye.",
    "You are the star in a single smile.", "You are the planet in a single heart.",
    "You are the world in a single soul.", "You are the everything in a single you.",
    "You are beautiful beyond measure.", "You are stunning beyond words.",
    "You are gorgeous beyond belief.", "You are pretty beyond comparison.",
    "You are lovely beyond limit.", "You are radiant beyond light.",
    "You are shining beyond stars.", "You are glowing beyond sun.",
    "You are bright beyond noon.", "You are clear beyond sky.",
    "You are soft beyond silk.", "You are hard beyond diamond.",
    "You are strong beyond mountain.", "You are deep beyond ocean.",
    "You are wide beyond horizon.", "You are high beyond peak.",
    "You are low beyond valley.", "You are near beyond heart.",
    "You are far beyond reach.", "You are here beyond presence.",
    "You are now beyond time.", "You are always beyond forever.",
    "You are the only one.", "You are the best one.",
    "You are the true one.", "You are the real one.",
    "You are the pure one.", "You are the clean one.",
    "You are the white one.", "You are the black one.",
    "You are the colors of the rainbow.", "You are the music of the spheres.",
    "You are the poetry of the heart.", "You are the art of the soul.",
    "You are the magic of the world.", "You are the miracle of life.",
    "You are the blessing of God.", "You are the gift of nature.",
    "You are the wonder of the universe.", "You are the treasure of the earth.",
    "You are the queen of my heart.", "You are the angel of my soul.",
    "You are the goddess of my world.", "You are the everything of my life."
]

def send_compliment():
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    
    logger.info(f"Starting ShYlpA compliment service at {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC ({now_ist.strftime('%Y-%m-%d %H:%M:%S')} IST)")
    
    try:
        logger.info("Initializing WhatsApp wrapper...")
        wrapper = WhatsAppWrapper()
        
        # Check instance state (optional, don't crash if this fails)
        try:
            state_resp = wrapper.client.account.getStateInstance()
            logger.info(f"Green API Instance State: {state_resp.data}")
        except Exception as e:
            logger.warning(f"Could not check instance state: {e}")
        
        # ShYlpA Jid (Reconstructed from previous logs)
        target_id = "919481546119@c.us" 
        message = random.choice(COMPLIMENTS)
        
        logger.info(f"Sending compliment: '{message}' to {target_id}")
        result = wrapper.send_message(target_id, message)
        logger.info(f"API Result: {result}")
        
        if "error" in result:
            logger.error(f"Green API Error: {result['error']}")
        elif result.get("status") == "success":
            success_msg = f"Compliment sent successfully! Message ID: {result.get('id')}"
            logger.info(success_msg)
            
            # Log to github_actions.txt for persistence
            try:
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                # Execution Log
                log_file = os.path.join(project_root, "github_actions.txt")
                with open(log_file, "a") as f:
                    f.write(f"[{now_ist.strftime('%Y-%m-%d %H:%M:%S')} IST] SUCCESS: {success_msg} | Message: '{message}'\n")
                
                # Dedicated Compliments Log
                compliments_file = os.path.join(project_root, "compliments.txt")
                with open(compliments_file, "a") as f:
                    f.write(f"[{now_ist.strftime('%Y-%m-%d %H:%M:%S')} IST] {message}\n")
                    
            except Exception as log_err:
                logger.warning(f"Failed to write to log files: {log_err}")
        else:
            logger.warning(f"Unexpected API response format: {result}")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    send_compliment()
