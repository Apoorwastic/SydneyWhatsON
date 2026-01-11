from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
import subprocess
import sys
from pathlib import Path

from api.load_csv_to_db import load_csv_to_db

BASE_DIR = Path(__file__).resolve().parent.parent
SCRAPER_PATH = BASE_DIR / "scraper" / "scrape_events.py"

_scheduler = None

def run_pipeline():
    print(f"[PIPELINE] Started at {datetime.now(timezone.utc)}")

    # 1️⃣ Run scraper
    subprocess.run(
        [sys.executable, str(SCRAPER_PATH)],
        check=False
    )

    # 2️⃣ Load CSV into DB
    load_csv_to_db()

    print(f"[PIPELINE] Finished at {datetime.now(timezone.utc)}")

def start_scheduler():
    global _scheduler

    if _scheduler:
        print("[SCHEDULER] Already running")
        return

    scheduler = BackgroundScheduler(timezone="UTC")

    scheduler.add_job(
        run_pipeline,
        trigger="interval",
        minutes=20,
        id="scraper_pipeline",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
    _scheduler = scheduler

    # 🔥 FORCE FIRST RUN IMMEDIATELY
    run_pipeline()

    print("[SCHEDULER] Started (runs every 20 minutes)")
