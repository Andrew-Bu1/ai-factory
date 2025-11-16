from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ModelBase(BaseModel):
    name: str
    provider: str
    model_id: str
    model_type: str
    description: Optional[str] = None
    max_tokens: Optional[int] = None
    input_cost_per_token: Optional[float] = None
    output_cost_per_token: Optional[float] = None
    context_window: Optional[int] = None
    dimension: Optional[int] = None
    is_active: bool = True


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model_id: Optional[str] = None
    model_type: Optional[str] = None
    description: Optional[str] = None
    max_tokens: Optional[int] = None
    input_cost_per_token: Optional[float] = None
    output_cost_per_token: Optional[float] = None
    context_window: Optional[int] = None
    dimension: Optional[int] = None
    is_active: Optional[bool] = None


class ModelResponse(ModelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


class ModelListResponse(BaseModel):
    items: list[ModelResponse]
    total: int
    page: int
    size: int
    pages: int