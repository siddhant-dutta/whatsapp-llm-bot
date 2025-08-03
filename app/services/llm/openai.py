# app/services/llm/openai.py

import httpx
from fastapi import HTTPException
from typing import List, Dict

from app.config import (
    OPENAI_API_BASE,
    OPENAI_MODEL,
    LLM_API_KEY,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE,
)
from app.services.llm.base import LLMClient, build_system_context

class OpenAIClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        self.api_key = api_key
        self.url = f"{OPENAI_API_BASE}/v1/chat/completions"

    async def generate(self, user_context: List[Dict[str, str]]) -> str:
        # Build messages with system prompt + user context
        messages = build_system_context(user_context)

        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "max_tokens": LLM_MAX_TOKENS,
            "temperature": LLM_TEMPERATURE,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(self.url, json=payload, headers=headers)

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Error from OpenAI API")

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Malformed response from OpenAI API")
