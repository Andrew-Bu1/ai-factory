from fastapi import APIRouter
from app.services.embedding_service import EmbeddingService
from app.api.schemas.embed import (
    EmbeddingRequest, 
    EmbeddingResponse,
    EmbeddingItem,
)
from app.api.deps import get_embedding_service
from fastapi import Depends
from app.api.errors import (
    NotFoundError, 
    APIError
)


router = APIRouter(tags=["Embedding"])

@router.post("/embed")
async def embed(
    payload: EmbeddingRequest, 
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> EmbeddingResponse:
    
    if not payload.model:
        raise NotFoundError("Model name must be provided")
    
    if not payload.input:
        raise NotFoundError("Input text must be provided")
    
    try:
        vectors = await embedding_service.embed(
            model=payload.model, inputs=payload.input
        )

        data = [
            EmbeddingItem(
                object="embedding",
                embedding=vector,
                index=i
            ) for i, vector in enumerate(vectors)
        ]

        return EmbeddingResponse(
            object="list",
            data=data,
            model=payload.model,
            usage={
                "prompt_tokens": 0,
                "total_tokens": 0
            }
        )        
    except Exception as e:
        raise APIError(detail=str(e))