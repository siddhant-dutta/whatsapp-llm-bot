# app/services/context/mongo.py
from datetime import datetime
from typing import List, Dict
from app.models.message import Message

from pymongo import MongoClient, ASCENDING, DESCENDING
from fastapi import HTTPException

from app.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, CONTEXT_LIMIT
from app.services.context.base import ContextRepository

class MongoContextRepository(ContextRepository):
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.col = self.db[MONGO_COLLECTION]
        # ensure index
        self.col.create_index([("user_id", ASCENDING), ("timestamp", DESCENDING)])

    def save_message(self, user_id: str, role: str, content: str):
        
        if not user_id or not content:
            raise HTTPException(400, "Invalid message data")
        
        msg = Message(user_id=user_id, role=role, content=content)
        self.col.insert_one(msg.to_mongo())

    def get_context(self, user_id: str, incoming_msg: str = "", limit: int = CONTEXT_LIMIT) -> List[Dict[str, str]]:
        if not user_id:
            return []
        docs = (
            self.col.find({"user_id": user_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        # reverse order
        return [Message.from_mongo(d) for d in reversed(list(docs))]
