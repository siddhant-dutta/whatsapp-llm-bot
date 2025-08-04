# app/services/transcription.py
import os
import requests
import tempfile
import whisper
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER 
from fastapi import HTTPException

# Load Whisper model once at import time
# You can switch "base" → "small", "medium" etc. to suit your accuracy/speed needs
_model = whisper.load_model("base")


def transcribe_audio_url(media_url: str) -> str:
    """
    Download the audio from the given URL (Twilio media URL),
    run Whisper transcription, and return the resulting text.
    Raises HTTPException on failure.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise HTTPException(500, "Twilio credentials not configured for media download")

    resp = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"Failed to download media: {media_url}")

    # Write to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name

    try:
        result = _model.transcribe(tmp_path)
        return result.get("text", "").strip()
    finally:
        # Clean up temp file
        try:
            os.remove(tmp_path)
        except OSError:
            pass
