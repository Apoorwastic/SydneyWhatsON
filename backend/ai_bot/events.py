import pandas as pd
import os

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "../scraper/sydney_events.csv"
)

df = pd.read_csv(CSV_PATH)

def find_events(keyword: str, limit=3):
    matches = df[
        df["title"].str.contains(keyword, case=False, na=False)
    ]
    return matches.head(limit)[["title", "venue", "ticket_url"]]
