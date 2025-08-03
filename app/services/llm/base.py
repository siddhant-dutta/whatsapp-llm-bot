# app/services/llm/base.py

from typing import Protocol, List, Dict

# Define a common interface for all LLM clients
class LLMClient(Protocol):
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Given a list of messages (role/content),
        return the assistant’s reply string.
        """
        ...

# Shared helper to prepend system prompt
from app.config import SYSTEM_PROMPT

def build_system_context(user_context: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Inserts the SYSTEM_PROMPT as the first message.
    """
    return [{"role": "system", "content": SYSTEM_PROMPT}] + user_context
