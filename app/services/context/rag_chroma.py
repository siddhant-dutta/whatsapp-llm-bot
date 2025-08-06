# app/services/context/rag.py
from app.services.context.base import ContextRepository
from app.models.rag_message import RAGMessage
from app.config import CONTEXT_LIMIT    

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb

from typing import List, Dict
from datetime import datetime
import uuid

class RAGContextRepository(ContextRepository):
    def __init__(self, persist_directory: str = "chroma_db"):
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="rag_context",
            embedding_function=self.embedding_function
        )

    def save_message(self, user_id: str, role: str, content: str) -> None:
        message = RAGMessage(
            user_id=user_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        )

        self.collection.add(
            documents=[message.content],
            metadatas=[message.to_metadata()],
            ids=[str(uuid.uuid4())]
        )

        # Prune messages after adding new one
        self.prune_old_messages(user_id)

    def get_context(self, user_id: str, incoming_msg: str, limit: int = CONTEXT_LIMIT) -> List[Dict[str, str]]:
        results = self.collection.query(
            query_texts=[incoming_msg],
            n_results=limit,
            where={"user_id": user_id}
        )

        messages = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            messages.append({
                "role": meta["role"],
                "content": doc
            })

        # Append the current user message at the end
        messages.append({"role": "user", "content": incoming_msg})
        return messages

    def prune_old_messages(self, user_id: str):
        # Retrieve all messages for the user (up to 100 for pruning)
        results = self.collection.query(
            query_texts=[""],
            n_results=100,
            where={"user_id": user_id}
        )

        if not results["metadatas"]:
            return

        # Sort messages by timestamp
        message_data = list(zip(results["ids"][0], results["metadatas"][0]))
        sorted_msgs = sorted(message_data, key=lambda x: x[1].get("timestamp", ""))

        # Keep only the latest CONTEXT_LIMIT messages
        if len(sorted_msgs) > 2*CONTEXT_LIMIT:
            ids_to_delete = [msg_id for msg_id, _ in sorted_msgs[:-2*CONTEXT_LIMIT]]
            self.collection.delete(ids=ids_to_delete)
            
        print(f"Pruned messages for user {user_id}. Remaining count: {len(sorted_msgs)}")  
