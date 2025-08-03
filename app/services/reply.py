# app/services/reply.py
import os
from twilio.rest import Client

# Load Twilio credentials from environment
ACCOUNT_SID      = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN       = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # e.g. "whatsapp:+14155238886"

# Initialize the Twilio client
_twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp_reply(to: str, body: str, media_url: str = None) -> str:
    """
    Send a WhatsApp message via Twilio.
    - to: recipient's WhatsApp number (e.g. "whatsapp:+91XXXXXXXXXX")
    - body: text message to send
    - media_url: (optional) URL of an image/audio to attach
    Returns the Twilio message SID.
    """
    params = {
        "from_": TWILIO_WHATSAPP_NUMBER,
        "to": to,
        "body": body
    }
    if media_url:
        # Twilio expects a list for media URLs
        params["media_url"] = [media_url]

    message = _twilio_client.messages.create(**params)
    return message.sid
