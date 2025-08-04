# app/routes/webhook.py
from fastapi import APIRouter, Request
from app.services.context.factory import get_context_repository
from app.services.llm.factory import get_llm_response
from app.services.reply import send_whatsapp_reply
from app.services.transcription import transcribe_audio_url

router = APIRouter()
repo = get_context_repository()

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Twilio calls this when a WhatsApp message arrives. Flow:
      1. Parse form data (text + optional media fields)
      2. If audio is attached: download & transcribe to text
      3. Save user message (text or transcript)
      4. Retrieve recent context
      5. Call LLM to generate a reply
      6. (Optional) generate TTS audio for the reply
      7. Send reply via Twilio (text + optional media)
      8. Save assistant reply
    """
    form = await request.form()
    user_number = form.get("From")       # e.g. "whatsapp:+91XXXXXXXXXX"
    incoming_msg = form.get("Body") or ""

    # Check for incoming voice note
    num_media    = int(form.get("NumMedia", 0))
    media_url    = form.get("MediaUrl0")          # Twilio media download URL
    media_type   = form.get("MediaContentType0")  # e.g. "audio/ogg"
    print(f"Received message from {user_number}: {incoming_msg} (Media: {num_media})")  

    # 1️⃣ Transcribe audio if present
    if num_media > 0 and media_url and media_type.startswith("audio"):
        incoming_msg = transcribe_audio_url(media_url)

    # 2. Build context for the LLM
    context_messages = repo.get_context(user_id=user_number, incoming_msg=incoming_msg)

    print(f"Context for {user_number}: {context_messages}")
    
    # 3️⃣ Call the LLM
    reply_text = await get_llm_response(context_messages)
    # reply_text = "This is a placeholder response from the LLM."
    print(f"LLM reply for {user_number}: {reply_text}")
    
    # 4️⃣ (Optional) generate TTS audio for reply
    audio_url = None
    # audio_url = await generate_tts_audio(reply_text)

    # 5️⃣ Send reply back via Twilio
    send_whatsapp_reply(to=user_number, body=reply_text, media_url=audio_url)

    # 6️⃣ Save the incoming message
    repo.save_message(user_number, "user", incoming_msg)
    
    # 7️⃣ Save assistant reply
    repo.save_message(user_number, "assistant", reply_text)

    return {"status": "ok"}
