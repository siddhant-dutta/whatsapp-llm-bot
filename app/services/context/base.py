# app/services/context/base.py
from abc import ABC, abstractmethod
from typing import List, Dict

class ContextRepository(ABC):
    @abstractmethod
    def save_message(self, user_id: str, role: str, content: str) -> None:
        """Persist a single message."""
        ...

    @abstractmethod
    def get_context(self, user_id: str, limit: int) -> List[Dict[str, str]]:
        """Fetch the last `limit` messages for a user."""
        ...
