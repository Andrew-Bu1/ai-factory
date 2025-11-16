from app.services.ai import LLMModel, EmbeddingModel
from functools import lru_cache
from app.core.config import settings

@lru_cache()
def get_llm_model() -> LLMModel:
    return LLMModel(
        base_url=settings.openrouter_base_url,
        api_key=settings.openrouter_api_key
    )

@lru_cache()
def get_embedding_model() -> EmbeddingModel:
    return EmbeddingModel()
