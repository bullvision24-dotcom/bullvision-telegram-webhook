from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "-1002278846520"
SECRET = os.getenv("SECRET", "bullvision")


@app.get("/")
def home():
    return {"status": "BullVision webhook online"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if data.get("secret") != SECRET:
        return {"status": "unauthorized"}

    msg_type = data.get("type", "")
    symbol = data.get("symbol", "N/A")
    direction = data.get("direction", "").upper()
    timeframe = data.get("timeframe", "N/A")

    if msg_type == "signal":
        emoji = "🟢" if direction == "BUY" else "🔴"

        message = f"""
{emoji} BULLVISION INDICATOR SIGNAL

📊 Asset: {symbol}
⏱ Timeframe: {timeframe}
📌 Direction: {direction}

🎯 Entry: {data.get("entry")}
🛑 Stop Loss: {data.get("sl")}

✅ TP1: {data.get("tp1")}
✅ TP2: {data.get("tp2")}
✅ TP3: {data.get("tp3")}

⚠️ Segnale automatico da TradingView
"""

    elif msg_type == "breakeven":
        message = f"""
⚡ BULLVISION BREAK EVEN

📊 Asset: {symbol}
📌 Direction: {direction}

🎯 Entry: {data.get("entry")}
🔐 Azione: Sposta SL a Break Even

⚠️ Alert automatico da TradingView
"""
    else:
        return {"status": "ignored"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return {"status": "sent"}
