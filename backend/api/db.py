import psycopg2
import os

def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
              id TEXT PRIMARY KEY,
              title TEXT,
              description TEXT,
              image_url TEXT,
              start_datetime TEXT,
              end_datetime TEXT,
              venue TEXT,
              city TEXT,
              category TEXT,
              ticket_url TEXT,
              source TEXT,
              source_event_id TEXT,
              hash TEXT UNIQUE,
              last_seen_at TEXT,
              created_at TEXT
            );
            """)
