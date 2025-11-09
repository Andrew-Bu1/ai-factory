from pydantic import BaseModel, Field


class ModelCreate(BaseModel):
    name: str = Field(default="deepseek", alias="Sample Name")
    description: str | None = Field(
        default="model of deepseek", alias="Sample Description"
    )
    is_active: bool = Field(default=True, alias="Active")


class ModelUpdate(BaseModel):
    name: str | None = Field(None, alias="Updated Name")
    description: str | None = Field(None, alias="Updated Description")
    is_active: bool | None = Field(None, alias="Active")


class ModelRead(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool | None
