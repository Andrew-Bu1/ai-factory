from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AIModelBase(BaseModel):
    name: str
    provider: str
    model_id: str
    model_type: str
    description: Optional[str] = None
    max_tokens: Optional[int] = None
    input_cost_per_token: Optional[float] = None
    output_cost_per_token: Optional[float] = None
    context_window: Optional[int] = None
    is_active: bool = True


class AIModelCreate(AIModelBase):
    pass


class AIModelUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model_id: Optional[str] = None
    model_type: Optional[str] = None
    description: Optional[str] = None
    max_tokens: Optional[int] = None
    input_cost_per_token: Optional[float] = None
    output_cost_per_token: Optional[float] = None
    context_window: Optional[int] = None
    is_active: Optional[bool] = None


class AIModelResponse(AIModelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


class AIModelListResponse(BaseModel):
    items: list[AIModelResponse]
    total: int
    page: int
    size: int
    pages: int