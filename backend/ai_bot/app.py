from fastapi import FastAPI, Request
import requests
import os
from bot import handle_message

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI()
print("BOT TOKEN LOADED:", bool(BOT_TOKEN))

@app.post("/telegram")
async def telegram_webhook(req: Request):
    data = await req.json()

    # ✅ SAFETY CHECK
    if "message" not in data:
        return {"ok": True}

    chat = data["message"].get("chat")
    text = data["message"].get("text")

    if not chat or not text:
        return {"ok": True}

    chat_id = chat["id"]
    reply = handle_message(chat_id, text)

    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return {"ok": True}
