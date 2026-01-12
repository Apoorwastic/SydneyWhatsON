from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys
import subprocess
import httpx
import pandas as pd
from pathlib import Path

# 🔥 MAKE backend/ IMPORTABLE
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from api.scheduler import start_scheduler
from bot import handle_message

# ---------------- PATHS ---------------- #

SCRAPER_PATH = ROOT_DIR / "scraper" / "scrape_events.py"
CSV_PATH = ROOT_DIR / "scraper" / "sydney_events.csv"

# ---------------- CONFIG ---------------- #

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_TOKEN = os.getenv("ADMIN_TRIGGER_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

print("BOT TOKEN LOADED:", bool(BOT_TOKEN))

# ---------------- LIFESPAN ---------------- #

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        start_scheduler()
        print("[API] Scheduler started")
    except Exception as e:
        print("[API] Scheduler failed:", e)

    yield

    print("[API] Shutting down")

# ---------------- APP ---------------- #

app = FastAPI(lifespan=lifespan)

# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sydneywhatson-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH ---------------- #

@app.get("/health")
async def health():
    return {"status": "ok"}

# ---------------- EVENTS ---------------- #

@app.get("/events")
async def get_events():
    if not CSV_PATH.exists():
        return {"count": 0, "events": []}

    df = pd.read_csv(CSV_PATH).fillna("")
    return {
        "count": len(df),
        "events": df.to_dict(orient="records")
    }

# ---------------- ADMIN SCRAPER TRIGGER ---------------- #

def run_scraper_process():
    print("[ADMIN] Scraper started")
    subprocess.run(
        [sys.executable, str(SCRAPER_PATH)],
        check=False
    )
    print("[ADMIN] Scraper finished")


@app.post("/admin/run-scraper")
async def run_scraper(
    background_tasks: BackgroundTasks,
    x_admin_token: str = Header(None)
):
    if not ADMIN_TOKEN or x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    background_tasks.add_task(run_scraper_process)

    return {
        "status": "started",
        "message": "Scraper running in background"
    }

# ---------------- TELEGRAM ---------------- #

@app.post("/telegram")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
    except Exception:
        return {"ok": True}

    if "message" not in data:
        return {"ok": True}

    chat = data["message"].get("chat")
    text = data["message"].get("text")

    if not chat or not text:
        return {"ok": True}

    chat_id = chat["id"]
    reply = handle_message(chat_id, text)

    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}
