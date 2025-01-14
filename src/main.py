import os
import time
import logging
import requests
from db import Database
from discord_notify import DiscordNotifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_studies():
    url = "https://atlasofpsychedelicresearch.com/atlas-query.php"
    params = {
        "filter_vars[phase]": "",
        "filter_vars[compound]": "",
        "filter_vars[topic]": "",
        "filter_vars[search]": ""
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['entries']

def main():
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    db = Database()
    notifier = DiscordNotifier()
    
    # Get existing studies from database
    existing_ids = set(db.get_existing_ids())
    logger.info(f"Found {len(existing_ids)} existing studies in database")
    
    # Fetch current studies from API
    current_studies = fetch_studies()
    logger.info(f"Fetched {len(current_studies)} studies from API")
    
    # Find new studies
    new_studies = 0
    for study_id, study_data in current_studies.items():
        study_id_int = int(study_id)
        if study_id_int not in existing_ids:
            logger.info(f"New study found: {study_data['post_title']}")
            # Insert new study into database
            db.insert_study(study_data)
            
            # Send Discord notification
            notifier.send_notification(study_data)
            new_studies += 1
    
    logger.info(f"Added {new_studies} new studies")

if __name__ == "__main__":
    main()