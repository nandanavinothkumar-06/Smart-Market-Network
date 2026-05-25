import requests
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/telegram", tags=["Telegram"])

# ⚙️ Replace these with your actual bot details
TELEGRAM_BOT_TOKEN = "8595205177:AAFrr0-RNqCPGvf9pGOt_It5H8X2qAke610"
TELEGRAM_CHAT_ID = "5965859600"

def send_telegram_notification(data: dict):
    """
    Sends a Telegram notification for a new order.
    """
    try:
        message = (
            f"📦 *New Order Alert!*\n"
            f"🧾 Order No: {data.get('order_no', 'N/A')}\n"
            f"👤 Customer ID: {data.get('customer_id')}\n"
            f"🏪 Retailer ID: {data.get('retailer_id')}\n"
            f"💰 Total: ₹{data.get('total')}\n"
            f"📍 Address: {data.get('address', 'N/A')}\n"
            f"🕒 Status: {data.get('status', 'Placed')}\n\n"
            f"🛍️ *Items:*\n"
        )

        for item in data.get("items", []):
            message += f"• {item.get('name', 'Unknown')} — {item.get('quantity')} × ₹{item.get('subtotal')}\n"

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data=payload
        )

        if response.status_code != 200:
            print("⚠️ Telegram API error:", response.text)
        else:
            print("✅ Telegram message sent successfully!")

    except Exception as e:
        print("⚠️ Telegram send failed:", e)


@router.post("/notify")
def telegram_notify(data: dict):
    """
    Public endpoint for Telegram notifications.
    """
    try:
        send_telegram_notification(data)
        return {"message": "Telegram notification sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
