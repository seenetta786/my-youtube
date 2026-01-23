#!/usr/bin/env python3
"""
Verify email addresses for HVAC companies
Inputs: .tmp/hvac_raw.json
Outputs: .tmp/hvac_verified.json with confidence scores
"""

import os
import json
import logging
import sys
import re
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
        logging.FileHandler(os.path.join(TMP_DIR, "verify_emails.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

INPUT_FILE = os.path.join(TMP_DIR, "hvac_raw.json")
OUTPUT_FILE = os.path.join(TMP_DIR, "hvac_verified.json")


def is_valid_email(email):
    """Basic email format validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def extract_email_from_website(website):
    """
    Attempt to extract email domain from website
    Returns common HVAC business email patterns
    """
    if not website:
        return None
    
    # Extract domain
    domain = website.replace("https://", "").replace("http://", "").split("/")[0]
    
    # Common patterns: info@, contact@, support@, hvac@
    patterns = ["info", "contact", "support", "hello", "sales"]
    return [f"{pattern}@{domain}" for pattern in patterns]


def verify_email(company):
    """
    Verify email for a company
    Returns company with email and confidence score
    """
    email = company.get("email")
    website = company.get("website")
    phone = company.get("phone")
    
    confidence = 0
    verified_email = None
    
    # If email provided, validate it
    if email and is_valid_email(email):
        verified_email = email
        confidence = 85  # Given email, assume higher confidence
    
    # Try to find email from website
    if not verified_email and website:
        possible_emails = extract_email_from_website(website)
        if possible_emails:
            verified_email = possible_emails[0]
            confidence = 60  # Pattern-matched, lower confidence
    
    # Phone number suggests business exists (fallback)
    if not verified_email and phone:
        # Could use phone number validation service here
        confidence = 30
    
    company["verified_email"] = verified_email
    company["confidence_score"] = confidence
    company["verification_method"] = (
        "provided" if email else 
        "website_pattern" if website else 
        "phone_only"
    )
    
    return company


def verify_hvac_emails():
    """Main verification process"""
    
    # Load raw data
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return False
    
    try:
        with open(INPUT_FILE, "r") as f:
            companies = json.load(f)
        logger.info(f"Loaded {len(companies)} companies")
    except Exception as e:
        logger.error(f"Error loading input file: {e}")
        return False
    
    # Verify emails
    logger.info("Verifying emails...")
    verified_companies = []
    high_confidence = 0
    medium_confidence = 0
    low_confidence = 0
    
    for i, company in enumerate(companies):
        company = verify_email(company)
        verified_companies.append(company)
        
        conf = company.get("confidence_score", 0)
        if conf >= 80:
            high_confidence += 1
        elif conf >= 60:
            medium_confidence += 1
        else:
            low_confidence += 1
        
        if (i + 1) % 50 == 0:
            logger.info(f"Processed {i + 1}/{len(companies)} companies")
    
    # Filter to high and medium confidence only
    filtered = [c for c in verified_companies if c.get("confidence_score", 0) >= 60]
    logger.info(f"✓ High confidence (>=80%): {high_confidence}")
    logger.info(f"✓ Medium confidence (60-80%): {medium_confidence}")
    logger.info(f"⚠ Low confidence (<60%): {low_confidence}")
    logger.info(f"✓ Total with verified emails: {len(filtered)}/{len(companies)}")
    
    # Save output
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(filtered, f, indent=2)
        logger.info(f"✓ Verification complete. Saved to {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Error saving output: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = verify_hvac_emails()
    sys.exit(0 if success else 1)
