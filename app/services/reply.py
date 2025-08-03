# app/services/reply.py
from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER  

# Initialize the Twilio client
_twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


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
