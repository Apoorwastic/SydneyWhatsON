import pandas as pd
from api.db import get_conn
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "scraper" / "sydney_events.csv"

def load_csv_to_db():
    if not CSV_PATH.exists():
        print("[DB] CSV not found, skipping DB load")
        return

    df = pd.read_csv(CSV_PATH)

    if df.empty:
        print("[DB] CSV empty, nothing to insert")
        return

    with get_conn() as conn:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute("""
                INSERT INTO events (
                  id, title, description, image_url,
                  start_datetime, end_datetime,
                  venue, city, category,
                  ticket_url, source,
                  source_event_id, hash,
                  last_seen_at, created_at
                ) VALUES (
                  %(id)s, %(title)s, %(description)s, %(image_url)s,
                  %(start_datetime)s, %(end_datetime)s,
                  %(venue)s, %(city)s, %(category)s,
                  %(ticket_url)s, %(source)s,
                  %(source_event_id)s, %(hash)s,
                  %(last_seen_at)s, %(created_at)s
                )
                ON CONFLICT (hash) DO UPDATE SET
                  last_seen_at = EXCLUDED.last_seen_at;
                """, row.to_dict())

        conn.commit()

    print(f"[DB] Loaded {len(df)} rows into database")
