#!/usr/bin/env python3
"""
Export HVAC company data to Google Sheet
Inputs: .tmp/hvac_final.json
Outputs: Google Sheet URL
"""

import os
import json
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        logging.FileHandler(os.path.join(TMP_DIR, "hvac_to_sheet.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

INPUT_FILE = os.path.join(TMP_DIR, "hvac_final.json")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def prepare_sheet_data(companies):
    """Convert company data to sheet format"""
    rows = []
    
    # Header row
    headers = [
        "Company Name",
        "Contact Name",
        "Email",
        "Phone",
        "Address",
        "City",
        "Website",
        "Services",
        "Company Size",
        "Confidence Score",
        "Notes"
    ]
    rows.append(headers)
    
    # Data rows
    for company in companies:
        row = [
            company.get("name", ""),
            company.get("contact_name", ""),
            company.get("verified_email", ""),
            company.get("phone", ""),
            company.get("address", ""),
            company.get("city", ""),
            company.get("website", ""),
            ", ".join(company.get("services", [])),
            company.get("company_size", ""),
            str(company.get("confidence_score", "")),
            company.get("verification_method", "")
        ]
        rows.append(row)
    
    return rows


def create_google_sheet(sheet_data):
    """Update existing Google Sheet with data"""
    try:
        # Load credentials
        creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        if not creds_file or not os.path.exists(creds_file):
            logger.error(f"Credentials file not found: {creds_file}")
            return None
        
        if not sheet_id:
            logger.error("GOOGLE_SHEETS_ID not set in .env")
            return None
        
        # Authenticate
        credentials = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        
        logger.info(f"Updating existing Google Sheet: {sheet_id}")
        
        # Prepare data for upload
        values = sheet_data
        
        # Clear existing data first
        logger.info("Clearing existing data...")
        service.spreadsheets().values().clear(
            spreadsheetId=sheet_id,
            range='Sheet1'
        ).execute()
        
        # Update sheet with data
        logger.info("Populating sheet with data...")
        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Sheet1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        logger.info(f"✓ Updated {result.get('updatedCells')} cells")
        
        # Format header row
        logger.info("Formatting header...")
        requests = [
            {
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {
                                'bold': True
                            },
                            'backgroundColor': {
                                'red': 0.8,
                                'green': 0.8,
                                'blue': 0.8
                            }
                        }
                    },
                    'fields': 'userEnteredFormat'
                }
            }
        ]
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={'requests': requests}
        ).execute()
        
        logger.info("✓ Formatted header row")
        
        # Generate share URL
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        logger.info(f"✓ Google Sheet updated: {sheet_url}")
        
        return sheet_url
        
    except HttpError as e:
        logger.error(f"Google API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error updating sheet: {e}")
        return None


def hvac_to_google_sheet():
    """Export to Google Sheet"""
    
    # Load final data
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return False
    
    try:
        with open(INPUT_FILE, "r") as f:
            companies = json.load(f)
        logger.info(f"Loaded {len(companies)} companies for sheet export")
    except Exception as e:
        logger.error(f"Error loading input file: {e}")
        return False
    
    # Prepare data
    logger.info("Formatting data for Google Sheet...")
    sheet_data = prepare_sheet_data(companies)
    
    # Create sheet
    sheet_url = create_google_sheet(sheet_data)
    
    if sheet_url:
        # Save URL to file for reference
        url_file = os.path.join(TMP_DIR, "sheet_url.txt")
        try:
            with open(url_file, "w") as f:
                f.write(sheet_url)
            logger.info(f"✓ Sheet URL saved to {url_file}")
        except Exception as e:
            logger.warning(f"Could not save URL file: {e}")
        
        logger.info("✓ Google Sheet export successful")
        return True
    else:
        logger.error("✗ Failed to create Google Sheet")
        return False


if __name__ == "__main__":
    success = hvac_to_google_sheet()
    sys.exit(0 if success else 1)
