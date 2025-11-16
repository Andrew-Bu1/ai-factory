from fastapi import APIRouter
from app.api.schemas.embed import (
    EmbeddingRequest, 
    EmbeddingResponse,
    EmbeddingItem,
)
from app.api.deps import get_embedding_model, EmbeddingModel
from fastapi import Depends
from app.api.errors import (
    NotFoundError, 
    APIError
)


router = APIRouter(tags=["Embedding"])

@router.post("/embeddings", response_model=EmbeddingResponse)
async def embed(
    payload: EmbeddingRequest, 
    embedding_model: EmbeddingModel = Depends(get_embedding_model)
) -> EmbeddingResponse:
    
    if not payload.model:
        raise NotFoundError("Model name must be provided")
    
    if not payload.inputs:
        raise NotFoundError("Input text must be provided")
    
    try:
        vectors = await embedding_model.infer(
            model_id=payload.model, inputs=payload.inputs
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