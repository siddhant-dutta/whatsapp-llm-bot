# app/config.py

import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

# Twilio settings
TWILIO_ACCOUNT_SID     = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN      = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

# Database settings
CONTEXT_BACKEND = os.getenv("CONTEXT_BACKEND", "mongo").lower()

# MongoDB settings
MONGO_DB        = os.getenv("MONGO_DB", "whatsapp_bot")
MONGO_USER      = os.getenv("MONGO_USER", "whatsappLLMBotUser")
MONGO_PASSWORD  = os.getenv("MONGO_PASSWORD", "Xt7olnUNJgGSg1Rg")
MONGO_HOST      = os.getenv("MONGO_HOST", "cluster0.zipds69.mongodb.net")
MONGO_COLLECTION= os.getenv("MONGO_COLLECTION", "messages")
CONTEXT_LIMIT   = int(os.getenv("CONTEXT_LIMIT", "10"))
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@"
    f"{MONGO_HOST}/{MONGO_DB}"
    "?retryWrites=true&w=majority"
)

# LLM settings
LLM_PROVIDER    = os.getenv("LLM_PROVIDER", "openai").lower()
LLM_API_KEY     = os.getenv("LLM_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com")
OPENAI_MODEL    = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
GROQ_API_BASE   = os.getenv("GROQ_API_BASE",   "https://api.groq.com/openai")
GROQ_MODEL      = os.getenv("GROQ_MODEL",      "llama-3.3-70b-versatile")
LLM_MAX_TOKENS  = int(os.getenv("LLM_MAX_TOKENS", "250"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Bot prompt
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are BucksBunny, a friendly financial assistant. Provide concise, actionable advice under 100 words."
)
