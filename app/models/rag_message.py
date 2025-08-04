# app/models/rag_message.py

from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class RAGMessage(BaseModel):
    user_id: str
    role: str
    content: str
    timestamp: datetime

    def to_metadata(self) -> Dict[str, Any]:
        """Convert message to metadata format for Chroma."""
        return {
            "user_id": self.user_id,
            "role": self.role,
            "timestamp": self.timestamp.isoformat()
        }