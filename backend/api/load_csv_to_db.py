import pandas as pd
from db import get_conn

CSV_PATH = "../scraper/sydney_events.csv"

def load_csv():
    df = pd.read_csv(CSV_PATH)

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
