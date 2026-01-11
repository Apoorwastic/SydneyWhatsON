from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import httpx

from bot import handle_message

# ---------------- CONFIG ---------------- #

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

print("BOT TOKEN LOADED:", bool(BOT_TOKEN))

# ---------------- APP ---------------- #

app = FastAPI()

# ---------------- CORS (IMPORTANT) ---------------- #
# Allows Netlify frontend to call Render backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sydneywhatson.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH CHECK ---------------- #

@app.get("/health")
async def health():
    return {"status": "ok"}

# ---------------- EVENTS API ---------------- #
# (Replace with real DB / CSV logic later)

@app.get("/events")
async def get_events():
    return {
        "events": [],
        "source": "api-alive"
    }

# ---------------- TELEGRAM WEBHOOK ---------------- #

@app.post("/telegram")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
    except Exception:
        # Invalid / empty body safety
        return {"ok": True}

    # Telegram safety check
    if "message" not in data:
        return {"ok": True}

    chat = data["message"].get("chat")
    text = data["message"].get("text")

    if not chat or not text:
        return {"ok": True}

    chat_id = chat["id"]

    # Your bot logic
    reply = handle_message(chat_id, text)

    # Async Telegram API call (NON-BLOCKING)
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

    return {"ok": True}
