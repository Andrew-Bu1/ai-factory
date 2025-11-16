from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.database import get_db
from app.repositories import ModelRepository
from app.api.schemas import ModelCreate, ModelUpdate, ModelResponse, ModelListResponse

router = APIRouter(prefix="/models", tags=["Models"])


def get_model_repository(db: Session = Depends(get_db)) -> ModelRepository:
    return ModelRepository(db)


@router.post("/", response_model=ModelResponse, status_code=201)
def create_model(
    model: ModelCreate,
    repository: ModelRepository = Depends(get_model_repository)
):
    """Create a new AI model"""
    # Check if model already exists
    existing_model = repository.get_by_model_id(model.model_id, model.provider)
    if existing_model:
        raise HTTPException(
            status_code=400,
            detail=f"AI model '{model.model_id}' from provider '{model.provider}' already exists"
        )
    
    return repository.create(model)


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: int,
    repository: ModelRepository = Depends(get_model_repository)
):
    """Get AI model by ID"""
    model = repository.get_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return model


@router.get("/", response_model=ModelListResponse)
def list_models(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    provider: Optional[str] = Query(None, description="Filter by provider"),
    model_type: Optional[str] = Query(None, description="Filter by model type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    repository: ModelRepository = Depends(get_model_repository)
):
    """List AI models with pagination and filtering"""
    skip = (page - 1) * size
    
    models = repository.get_all(
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
    
    return ModelListResponse(
        items=models,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.put("/{model_id}", response_model=ModelResponse)
def update_model(
    model_id: int,
    model_update: ModelUpdate,
    repository: ModelRepository = Depends(get_model_repository)
):
    """Update an AI model"""
    model = repository.update(model_id, model_update)
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return model


@router.delete("/{model_id}", status_code=204)
def delete_model(
    model_id: int,
    soft: bool = Query(False, description="Soft delete (deactivate) instead of hard delete"),
    repository: ModelRepository = Depends(get_model_repository)
):
    """Delete an AI model"""
    if soft:
        model = repository.soft_delete(model_id)
        if not model:
            raise HTTPException(status_code=404, detail="AI model not found")
    else:
        success = repository.delete(model_id)
        if not success:
            raise HTTPException(status_code=404, detail="AI model not found")


@router.post("/{model_id}/activate", response_model=ModelResponse)
def activate_model(
    model_id: int,
    repository: ModelRepository = Depends(get_model_repository)
):
    """Activate an AI model"""
    model = repository.update(model_id, ModelUpdate(is_active=True))
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return model


@router.post("/{model_id}/deactivate", response_model=ModelResponse)
def deactivate_model(
    model_id: int,
    repository: ModelRepository = Depends(get_model_repository)
):
    """Deactivate an AI model"""
    model = repository.update(model_id, ModelUpdate(is_active=False))
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return model