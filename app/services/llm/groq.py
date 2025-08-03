# app/services/llm/groq.py

import os
import httpx
from fastapi import HTTPException
from typing import List, Dict
from app.services.llm.base import LLMClient, build_system_context

GROQ_BASE = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "250"))
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

class GroqClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise HTTPException(500, "Groq API key not configured")
        self.api_key = api_key
        self.url = f"{GROQ_BASE}/v1/chat/completions"

    async def generate(self, user_context: List[Dict[str, str]]) -> str:
        messages = build_system_context(user_context)
        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(self.url, json=payload, headers=headers)

        if resp.status_code != 200:
            raise HTTPException(resp.status_code, "Error from Groq API")

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            raise HTTPException(500, "Malformed response from Groq API")
