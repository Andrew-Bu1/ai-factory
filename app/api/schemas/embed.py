from pydantic import BaseModel, Field
from typing import List


class EmbeddingRequest(BaseModel):
    model: str = Field(
        ...,
        example="text-embedding-3-small",
        description="The model to use for generating embeddings.",
    )
    input: List[str] | str = Field(
        ...,
        example=["Your text string goes here", "Another text string"],
        description="Input text(s) to generate embeddings for.",
    )


class EmbeddingItem(BaseModel):
    object: str = Field(
        "embedding", example="embedding", description="The type of object returned."
    )
    embedding: List[float] = Field(
        ..., example=[0.1, 0.2, 0.3, 0.4], description="The generated embedding vector."
    )
    index: int = Field(
        ...,
        example=0,
        description="The index of the input text corresponding to this embedding.",
    )


class Usage(BaseModel):
    prompt_tokens: int = Field(
        ..., example=10, description="The number of tokens in the input text."
    )
    total_tokens: int = Field(
        ..., example=10, description="The total number of tokens processed."
    )


class EmbeddingResponse(BaseModel):
    object: str = Field(
        "list", example="list", description="The type of object returned."
    )
    data: List[EmbeddingItem] = Field(..., description="List of embedding items.")
    model: str = Field(
        ...,
        example="text-embedding-3-small",
        description="The model used for generating embeddings.",
    )
    usage: Usage = Field(..., description="Token usage information.")
