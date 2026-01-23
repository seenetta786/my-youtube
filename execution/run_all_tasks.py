import os
import sys
import logging

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.clickup_create_task import create_task
from execution.recurring_rcb_poll import run_rcb_poll

LEAD_NAME = "Nick Sar"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_lead_in_clickup():
    """Creates a new lead in ClickUp."""
    list_id = os.getenv("CLICKUP_LIST_ID")
    if not list_id:
        logging.error("CLICKUP_LIST_ID not found in .env file. Please add it and try again.")
        logging.info("You can find the List ID by running: python3 execution/discover_clickup.py")
        return

    logging.info(f"Attempting to create a new lead '{LEAD_NAME}' in ClickUp list '{list_id}'...")
    try:
        task = create_task(list_id, LEAD_NAME)
        if task and 'id' in task:
            logging.info(f"Successfully created lead with ID: {task['id']}")
        else:
            logging.error(f"Failed to create lead. Response: {task}")
    except Exception as e:
        logging.error(f"An error occurred while creating the lead: {e}")

def run_whatsapp_poll():
    """Runs the RCB poll on WhatsApp."""
    logging.info("Attempting to run the RCB poll...")
    try:
        run_rcb_poll()
        logging.info("RCB poll script finished.")
    except Exception as e:
        logging.error(f"An error occurred while running the RCB poll: {e}")

if __name__ == "__main__":
    logging.info("Starting the task execution script...")
    
    # 1. Create the lead in ClickUp
    create_lead_in_clickup()
    
    # 2. Run the WhatsApp poll
    run_whatsapp_poll()
    
    logging.info("All tasks completed.")
