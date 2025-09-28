from app.services.embedding_service import EmbeddingService
from app.services.chat_service import ChatService
from functools import lru_cache
from app.core.config import settings

@lru_cache()
def get_chat_service() -> ChatService:
    return ChatService(
        base_url=settings.openrouter_base_url,
        api_key=settings.openrouter_api_key
    )

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
