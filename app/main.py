# app/main.py

import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Import the Twilio webhook router
from app.routes.webhook import router as webhook_router

# Create FastAPI app
app = FastAPI(
    title="BucksBunny WhatsApp Bot",
    description="A voice/text-enabled WhatsApp chatbot for financial literacy with context tracking",
    version="1.0.0"
)

# Include the webhook route (handles POST /webhook)
app.include_router(webhook_router, prefix="")

# Health check endpoint
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# If you run this module directly, start Uvicorn
if __name__ == "__main__":
    import uvicorn

    # Port can be set via PORT env var (Render/Railway defaults to 8000)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
