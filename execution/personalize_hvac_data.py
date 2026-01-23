#!/usr/bin/env python3
"""
Personalize HVAC company data
Inputs: .tmp/hvac_verified.json
Outputs: .tmp/hvac_final.json with enriched data
"""

import os
import json
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv

# Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
TMP_DIR = os.path.join(BASE_DIR, ".tmp")
os.makedirs(TMP_DIR, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(TMP_DIR, "personalize_hvac.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

INPUT_FILE = os.path.join(TMP_DIR, "hvac_verified.json")
OUTPUT_FILE = os.path.join(TMP_DIR, "hvac_final.json")


def personalize_company(company):
    """
    Add personalization fields to company data
    """
    # Extract name for potential contact field
    company_name = company.get("name", "")
    
    # Infer common personalization data
    # In production, would scrape website or use LinkedIn API
    company["contact_name"] = f"Manager at {company_name.split()[0]}"  # Placeholder
    company["services"] = ["HVAC Installation", "Maintenance", "Repair"]  # Generic default
    company["company_size"] = "Small-Medium"  # Placeholder
    company["years_in_business"] = "Unknown"  # Would research from website
    company["website_title"] = company_name  # Could scrape from <title> tag
    
    # Email personalization fields (for template use)
    company["email_field_company"] = company.get("name", "Company")
    company["email_field_contact"] = company.get("contact_name", "Contact")
    company["email_field_services"] = ", ".join(company.get("services", ["HVAC Services"]))
    
    return company


def personalize_hvac_data():
    """Main personalization process"""
    
    # Load verified data
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return False
    
    try:
        with open(INPUT_FILE, "r") as f:
            companies = json.load(f)
        logger.info(f"Loaded {len(companies)} verified companies")
    except Exception as e:
        logger.error(f"Error loading input file: {e}")
        return False
    
    # Personalize each company
    logger.info("Adding personalization data...")
    personalized = []
    
    for i, company in enumerate(companies):
        try:
            company = personalize_company(company)
            personalized.append(company)
        except Exception as e:
            logger.warning(f"Error personalizing {company.get('name', 'Unknown')}: {e}")
            personalized.append(company)  # Still include, but with error
        
        if (i + 1) % 50 == 0:
            logger.info(f"Personalized {i + 1}/{len(companies)}")
    
    # Save output
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(personalized, f, indent=2)
        logger.info(f"✓ Personalization complete. Saved to {OUTPUT_FILE}")
        logger.info(f"✓ Ready for Google Sheet export")
    except Exception as e:
        logger.error(f"Error saving output: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = personalize_hvac_data()
    sys.exit(0 if success else 1)
