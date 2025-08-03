# app/services/llm/factory.py

from fastapi import HTTPException
from typing import List, Dict

from app.config import LLM_PROVIDER, LLM_API_KEY
from app.services.llm.base import LLMClient
from app.services.llm.openai import OpenAIClient
from app.services.llm.groq import GroqClient

def get_llm_client() -> LLMClient:
    """
    Return an instance of the configured LLM client.
    """
    provider = LLM_PROVIDER.lower()
    api_key  = LLM_API_KEY

    if provider == "openai":
        return OpenAIClient(api_key)
    elif provider == "groq":
        return GroqClient(api_key)
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Unsupported LLM provider '{provider}'"
        )

async def get_llm_response(context: List[Dict[str, str]]) -> str:
    """
    Build the proper client and return its generated reply for the given context.
    """
    client = get_llm_client()
    return await client.generate(context)
