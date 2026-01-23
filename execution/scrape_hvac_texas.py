#!/usr/bin/env python3
"""
Scrape HVAC companies in Texas from multiple sources
Outputs: .tmp/hvac_raw.json with company data
"""

import os
import json
import time
import logging
import sys
import requests
from datetime import datetime
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
        logging.FileHandler(os.path.join(TMP_DIR, "scrape_hvac.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

OUTPUT_FILE = os.path.join(TMP_DIR, "hvac_raw.json")
CHECKPOINT_FILE = os.path.join(TMP_DIR, "hvac_raw_checkpoint.json")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def load_checkpoint():
    """Load previous scraping checkpoint if exists"""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r") as f:
                data = json.load(f)
            logger.info(f"Loaded checkpoint with {len(data)} records")
            return data
        except Exception as e:
            logger.warning(f"Could not load checkpoint: {e}")
    return []


def save_checkpoint(companies):
    """Save current progress"""
    try:
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(companies, f, indent=2)
        logger.info(f"Checkpoint saved with {len(companies)} records")
    except Exception as e:
        logger.error(f"Error saving checkpoint: {e}")


def deduplicate_companies(companies):
    """Remove duplicate companies by name + city"""
    seen = set()
    unique = []
    for company in companies:
        key = (company.get("name", "").lower(), company.get("city", "").lower())
        if key and key not in seen:
            seen.add(key)
            unique.append(company)
    return unique


def scrape_hvac_companies():
    """
    Scrape HVAC companies from Google Maps using SerpAPI
    """
    companies = load_checkpoint()
    
    logger.info("Starting HVAC company scraping for Texas...")
    logger.info("Target: 200 companies")
    
    if not SERPAPI_KEY:
        logger.error("SERPAPI_KEY not found in .env")
        return False
    
    # Phase 1: Google Maps via SerpAPI - Multiple cities in Texas
    logger.info("Phase 1: Scraping Google Maps via SerpAPI...")
    
    texas_cities = [
        "Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "Arlington",
        "Corpus Christi", "Plano", "Lubbock", "Garland", "Irving", "Laredo",
        "Amarillo", "Frisco", "Grand Prairie", "Brownsville", "Pasadena",
        "McKinney", "Killeen", "Mesquite", "Beaumont", "Waco", "Carrollton",
        "Midland", "Denton", "Abilene", "Odessa", "Round Rock", "Wichita Falls",
        "Richardson"
    ]
    
    try:
        for city in texas_cities:
            logger.info(f"Scraping {city}, TX...")
            
            # SerpAPI Google Maps search - correct format
            params = {
                "q": f"HVAC companies {city} TX",
                "api_key": SERPAPI_KEY,
                "engine": "google"  # Use google engine
            }
            
            try:
                response = requests.get("https://serpapi.com/search", params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Extract organic results
                if "organic_results" in data:
                    for result in data["organic_results"][:100]:  # Limit 100 per city
                        # Extract company info from organic results
                        title = result.get("title", "")
                        link = result.get("link", "")
                        
                        # Try to extract phone from snippet
                        snippet = result.get("snippet", "")
                        
                        company = {
                            "name": title,
                            "address": snippet[:100] if snippet else "",
                            "city": city,
                            "state": "TX",
                            "phone": "",
                            "website": link,
                            "email": None,
                            "rating": "",
                            "review_count": "",
                            "source": "google_serpapi"
                        }
                        
                        # Only add if has a name
                        if title and "hvac" in title.lower():
                            companies.append(company)
                        
                    logger.info(f"  ✓ Added results from {city}")
                
                # Respect API rate limits
                time.sleep(0.3)
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"  ⚠ Error scraping {city}: {e}")
                continue
        
        logger.info(f"Phase 1 complete: {len(companies)} companies collected")
        
    except Exception as e:
        logger.error(f"Error in Phase 1: {e}")
    
    # Deduplicate and save
    companies = deduplicate_companies(companies)
    save_checkpoint(companies)
    
    # Save to final output
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(companies, f, indent=2)
        logger.info(f"✓ Scraping complete. Saved {len(companies)} companies to {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Error saving output file: {e}")
        return False
    
    # Status report
    if len(companies) < 100:
        logger.warning(f"⚠ Only scraped {len(companies)} companies, target was 200")
    else:
        logger.info(f"✓ Successfully scraped {len(companies)} unique companies")
    
    return True


if __name__ == "__main__":
    success = scrape_hvac_companies()
    sys.exit(0 if success else 1)
