from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.database import get_db
from app.repositories import AIModelRepository
from app.api.schemas import AIModelCreate, AIModelUpdate, AIModelResponse, AIModelListResponse

router = APIRouter(prefix="/models", tags=["AI Models"])


def get_ai_model_repository(db: Session = Depends(get_db)) -> AIModelRepository:
    return AIModelRepository(db)


@router.post("/", response_model=AIModelResponse, status_code=201)
def create_ai_model(
    ai_model: AIModelCreate,
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """Create a new AI model"""
    # Check if model already exists
    existing_model = repository.get_by_model_id(ai_model.model_id, ai_model.provider)
    if existing_model:
        raise HTTPException(
            status_code=400,
            detail=f"AI model '{ai_model.model_id}' from provider '{ai_model.provider}' already exists"
        )
    
    return repository.create(ai_model)


@router.get("/{model_id}", response_model=AIModelResponse)
def get_ai_model(
    model_id: int,
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """Get AI model by ID"""
    ai_model = repository.get_by_id(model_id)
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return ai_model


@router.get("/", response_model=AIModelListResponse)
def list_ai_models(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    provider: Optional[str] = Query(None, description="Filter by provider"),
    model_type: Optional[str] = Query(None, description="Filter by model type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """List AI models with pagination and filtering"""
    skip = (page - 1) * size
    
    ai_models = repository.get_all(
        skip=skip,
        limit=size,
        provider=provider,
        model_type=model_type,
        is_active=is_active
    )
    
    total = repository.count(
        provider=provider,
        model_type=model_type,
        is_active=is_active
    )
    
    pages = math.ceil(total / size) if total > 0 else 1
    
    return AIModelListResponse(
        items=ai_models,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.put("/{model_id}", response_model=AIModelResponse)
def update_ai_model(
    model_id: int,
    ai_model_update: AIModelUpdate,
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """Update an AI model"""
    ai_model = repository.update(model_id, ai_model_update)
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return ai_model


@router.delete("/{model_id}", status_code=204)
def delete_ai_model(
    model_id: int,
    soft: bool = Query(False, description="Soft delete (deactivate) instead of hard delete"),
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """Delete an AI model"""
    if soft:
        ai_model = repository.soft_delete(model_id)
        if not ai_model:
            raise HTTPException(status_code=404, detail="AI model not found")
    else:
        success = repository.delete(model_id)
        if not success:
            raise HTTPException(status_code=404, detail="AI model not found")


@router.post("/{model_id}/activate", response_model=AIModelResponse)
def activate_ai_model(
    model_id: int,
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """Activate an AI model"""
    ai_model = repository.update(model_id, AIModelUpdate(is_active=True))
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return ai_model


@router.post("/{model_id}/deactivate", response_model=AIModelResponse)
def deactivate_ai_model(
    model_id: int,
    repository: AIModelRepository = Depends(get_ai_model_repository)
):
    """Deactivate an AI model"""
    ai_model = repository.update(model_id, AIModelUpdate(is_active=False))
    if not ai_model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return ai_model