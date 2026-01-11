from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
import subprocess
import sys
import os

# Base directory: backend/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Path to scraper script
SCRAPER_PATH = os.path.join(BASE_DIR, "scraper", "scrape_events.py")

def run_scraper():
    print(f"[SCHEDULER] Running scraper at {datetime.now(timezone.utc)}")

    subprocess.run(
        [sys.executable, SCRAPER_PATH],
        check=False
    )

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")

    scheduler.add_job(
        run_scraper,
        trigger="interval",
        minutes=20,              # 🔥 EVERY 20 MINUTES
        id="event_scraper",
        replace_existing=True,
        max_instances=1          # 🔒 prevent overlap runs
    )

    scheduler.start()
    print("[SCHEDULER] Started (runs every 20 minutes)")
