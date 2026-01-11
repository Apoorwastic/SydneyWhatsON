from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SCRAPER_PATH = os.path.join(BASE_DIR, "scraper", "scrape_events.py")

def run_scraper():
    print(f"[SCHEDULER] Running scraper at {datetime.utcnow()}")

    subprocess.run(
        [sys.executable, SCRAPER_PATH],
        check=False
    )

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        run_scraper,
        trigger="interval",
        hours=1,          # 🔥 EVERY 1 HOUR
        id="event_scraper",
        replace_existing=True
    )
    scheduler.start()

    print("[SCHEDULER] Started (runs every 1 hour)")
