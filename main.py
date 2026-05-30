```python
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


def clean_symbol(symbol):
    symbol = str(symbol).upper()

    if "XAU" in symbol:
        return "XAU"
    elif "BTC" in symbol:
        return "BTC"
    elif "ETH" in symbol:
        return "ETH"

    return symbol.replace("USD", "")


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if data.get("secret") != SECRET:
        return {"status": "unauthorized"}

    msg_type = str(data.get("type", "")).lower()

    symbol = clean_symbol(data.get("symbol", "N/A"))
    direction = str(data.get("direction", "")).upper()

    entry = data.get("entry", "")
    sl = data.get("sl", "")

    tp1 = data.get("tp1", "")
    tp2 = data.get("tp2", "")
    tp3 = data.get("tp3", "")

    if msg_type == "signal":

        emoji = "🟢" if direction == "BUY" else "🔴"

        message = f"""
{emoji} BV-SIGNAL

📈 {symbol} {direction}

🎯 ENTRY: {entry}
🛑 SL: {sl}

✅ TP1: {tp1}
✅ TP2: {tp2}
✅ TP3: {tp3}
"""

    elif msg_type == "breakeven":

        message = f"""
⚡ BV-SIGNAL BREAK EVEN

📈 {symbol} {direction}

🎯 ENTRY: {entry}

🔐 AZIONE: SPOSTA SL A BE
"""

    else:
        return {"status": "ignored"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message.strip()
        }
    )

    return {
        "status": "sent",
        "telegram_status": response.status_code,
        "telegram_response": response.text
    }
```
