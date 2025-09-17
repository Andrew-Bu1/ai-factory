from fastapi import APIRouter, Depends
from ..schemas.llm import LLMRequest, LLMResponse
from typing import Any

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=LLMResponse)
async def chat():
    return  