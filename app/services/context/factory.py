# app/services/context/factory.py
import os

from fastapi import HTTPException
from app.services.context.base import ContextRepository
from app.services.context.mongo import MongoContextRepository 
from app.services.context.rag_chroma import RAGContextRepository  # future
from app.config import CONTEXT_BACKEND
# from app.services.context.redis import RedisContextRepository  # future

def get_context_repository() -> ContextRepository:
    
    if CONTEXT_BACKEND == "mongo":
        return MongoContextRepository()
    elif CONTEXT_BACKEND == "rag":
        return RAGContextRepository()
    else:
        raise HTTPException(500, f"Unsupported CONTEXT_BACKEND '{CONTEXT_BACKEND}' configured")
