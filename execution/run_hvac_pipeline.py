#!/usr/bin/env python3
"""
Orchestration script for HVAC scraping workflow
Runs all phases: Scrape → Verify → Personalize → Export
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXECUTION_DIR = os.path.join(BASE_DIR, "execution")
TMP_DIR = os.path.join(BASE_DIR, ".tmp")

# Setup logging
os.makedirs(TMP_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(TMP_DIR, "hvac_workflow.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_phase(script_name, phase_name):
    """Run a phase script and return success status"""
    logger.info(f"\n{'='*60}")
    logger.info(f"PHASE: {phase_name}")
    logger.info(f"{'='*60}")
    
    script_path = os.path.join(EXECUTION_DIR, script_name)
    
    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
        return False
    
    try:
        # Use the venv python if available
        python_exe = os.path.join(BASE_DIR, ".venv", "bin", "python")
        if not os.path.exists(python_exe):
            python_exe = sys.executable
        
        result = subprocess.run(
            [python_exe, script_path],
            capture_output=False,
            timeout=300  # 5 minute timeout per phase
        )
        
        if result.returncode == 0:
            logger.info(f"✓ {phase_name} completed successfully")
            return True
        else:
            logger.error(f"✗ {phase_name} failed with return code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"✗ {phase_name} timed out (>5 minutes)")
        return False
    except Exception as e:
        logger.error(f"✗ {phase_name} error: {e}")
        return False


def main():
    logger.info("Starting HVAC Company Outreach Pipeline")
    logger.info(f"Base directory: {BASE_DIR}")
    logger.info(f"Output directory: {TMP_DIR}")
    
    phases = [
        ("scrape_hvac_texas.py", "Phase 1: Scrape HVAC Companies"),
        ("verify_hvac_emails.py", "Phase 2: Verify Email Addresses"),
        ("personalize_hvac_data.py", "Phase 3: Personalize Company Data"),
        ("hvac_to_google_sheet.py", "Phase 4: Export to Google Sheet"),
    ]
    
    completed = 0
    failed = 0
    
    for script, phase_name in phases:
        if run_phase(script, phase_name):
            completed += 1
        else:
            failed += 1
            # For graceful recovery, continue to next phase if possible
            logger.warning(f"⚠ Continuing to next phase despite error...")
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("WORKFLOW SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"✓ Completed: {completed}/{len(phases)}")
    logger.info(f"✗ Failed: {failed}/{len(phases)}")
    
    if completed == len(phases):
        logger.info("✓ Pipeline completed successfully!")
        logger.info(f"\nOutputs:")
        logger.info(f"  - Raw data: {os.path.join(TMP_DIR, 'hvac_raw.json')}")
        logger.info(f"  - Verified: {os.path.join(TMP_DIR, 'hvac_verified.json')}")
        logger.info(f"  - Final: {os.path.join(TMP_DIR, 'hvac_final.json')}")
        logger.info(f"  - Sheet: [Awaiting Google API setup]")
        return 0
    else:
        logger.error(f"✗ Pipeline incomplete. Check logs for errors.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
