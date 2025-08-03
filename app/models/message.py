# app/models/message.py

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    A chat message, either from the user or the assistant.
    This model can be used to validate input/output or
    to convert MongoDB documents into typed objects.
    """
    user_id: str = Field(
        ..., description="WhatsApp identifier, e.g. 'whatsapp:+91XXXXXXXXXX'"
    )
    role: Literal["user", "assistant"] = Field(
        ..., description="Who sent the message"
    )
    content: str = Field(..., description="The text content of the message")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC time when this message was created"
    )

    @classmethod
    def from_mongo(cls, doc: dict) -> "Message":
        """
        Create a Message from a raw MongoDB document.
        Strips out the '_id' field and casts timestamp.
        """
        data = {
            "user_id": doc["user_id"],
            "role": doc["role"],
            "content": doc["content"],
            "timestamp": doc["timestamp"],
        }
        return cls(**data)

    def to_mongo(self) -> dict:
        """
        Prepare this Message for insertion into MongoDB.
        """
        return {
            "user_id": self.user_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }
