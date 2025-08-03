# app/routes/webhook.py
from fastapi import APIRouter, Request
from app.services.context.factory import get_context_repository
from app.services.llm.factory import get_llm_response
from app.services.reply import send_whatsapp_reply

router = APIRouter()
repo = get_context_repository()

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    This endpoint is called by Twilio whenever a WhatsApp message arrives.
    It:  
      1. Reads the incoming message and sender number
      2. Stores the user message in MongoDB
      3. Retrieves recent history for context
      4. Calls the LLM to generate a reply
      5. Stores the bot reply in MongoDB
      6. Sends the reply back via Twilio
    """
    form = await request.form()
    user_number = form.get("From")       # e.g. "whatsapp:+91XXXXXXXXXX"
    incoming_msg = form.get("Body") or "" # user’s text message

    # 1. Save the incoming user message
    repo.save_message(user_number, "user", incoming_msg)

    # 2. Fetch recent context (last N messages)
    context_messages = repo.get_context(user_number)

    # 3. Append the latest user message for the LLM prompt
    context_messages.append({"role": "user", "content": incoming_msg})

    # 4. Get a response from the LLM
    # reply_text = await get_llm_response(context_messages)

    # 5. Save the assistant’s reply
    # repo.save_message(user_number, "assistant", reply_text)

    # 6. Send the reply back on WhatsApp
    # send_whatsapp_reply(to=user_number, body=reply_text)

    return {"status": "ok"}
