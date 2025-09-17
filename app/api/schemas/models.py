from typing import Optional
from pydantic import BaseModel, Field


class ModelCreate(BaseModel):
    name: str = Field(..., example="Sample Name")
    description: Optional[str] = Field(None, example="Sample Description")
    is_active: bool = Field(True, example=True)

class ModelUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Name")
    description: Optional[str] = Field(None, example="Updated Description")
    is_active: Optional[bool] = Field(None, example=False)

class ModelRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool

