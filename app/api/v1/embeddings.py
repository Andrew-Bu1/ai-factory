from fastapi import APIRouter
from app.services.embedding_service import EmbeddingService
from app.core.config import settings

router = APIRouter()

@router.post("/embed")
async def embed():
    return