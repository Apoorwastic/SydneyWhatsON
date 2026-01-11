from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
import subprocess
import sys
import os
from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# backend/scraper/scrape_events.py
SCRAPER_PATH = BASE_DIR / "scraper" / "scrape_events.py"

_scheduler = None  # prevent duplicate schedulers


def run_scraper():
    print(f"[SCHEDULER] Running scraper at {datetime.now(timezone.utc)}")

    subprocess.run(
        [sys.executable, str(SCRAPER_PATH)],
        check=False
    )


def start_scheduler():
    global _scheduler

    if _scheduler:
        print("[SCHEDULER] Already running, skipping duplicate start")
        return

    scheduler = BackgroundScheduler(timezone="UTC")

    scheduler.add_job(
        run_scraper,
        trigger="interval",
        minutes=20,
        id="event_scraper",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
    _scheduler = scheduler

    print("[SCHEDULER] Started (runs every 20 minutes)")
