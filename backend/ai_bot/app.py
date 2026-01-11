from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import subprocess
import httpx
import pandas as pd
from pathlib import Path

from bot import handle_message

# ---------------- PATH SETUP ---------------- #

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
SCRAPER_PATH = BASE_DIR / "scraper" / "scrape_events.py"
CSV_PATH = BASE_DIR / "scraper" / "sydney_events.csv"

# ---------------- CONFIG ---------------- #

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_TOKEN = os.getenv("ADMIN_TRIGGER_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

print("BOT TOKEN LOADED:", bool(BOT_TOKEN))

# ---------------- APP ---------------- #

app = FastAPI()

# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sydneywhatson.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH ---------------- #

@app.get("/health")
async def health():
    return {"status": "ok"}

# ---------------- EVENTS API ---------------- #

@app.get("/events")
async def get_events():
    if not CSV_PATH.exists():
        return {"events": []}

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

# ---------------- TELEGRAM WEBHOOK ---------------- #

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
