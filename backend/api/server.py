from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pandas as pd
import os

from scheduler import start_scheduler   # 🔥 NEW

BASE_DIR = os.path.dirname(__file__)
CSV = os.path.join(BASE_DIR, "../scraper/sydney_events.csv")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 Start hourly scraper when API starts
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/events")
def events():
    df = pd.read_csv(CSV)

    # ❌ DO NOT PARSE DATES ANYMORE (THEY ARE STRINGS)
    df = df.sort_values("created_at", ascending=False)

    return df.fillna("").to_dict(orient="records")
