from .chat import router as chat_router
from .embeddings import router as embed_router
from fastapi import (
    APIRouter
)
router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(chat_router)
router_v1.include_router(embed_router)
