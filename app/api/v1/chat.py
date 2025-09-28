from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from ..schemas.llm import (
    LLMRequest, 
    LLMResponse
)
from app.api.errors import (
    APIError
)
from app.services.chat_service import ChatService
from app.api.deps import get_chat_service
from typing import Union

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat", 
    response_model=LLMResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": LLMResponse.model_json_schema()
                },
                "text/event-stream": {
                    "schema": {
                        "type": "string",
                        "example": "data: {\"id\": \"chatcmpl-123\", \"object\": \"chat.completion.chunk\", \"created\": 1677652288, \"model\": \"gpt-3.5-turbo-0301\", \"choices\": [{\"delta\": {\"role\": \"assistant\", \"content\": \"Hello! How can I assist you today?\"}, \"index\": 0, \"finish_reason\": null}]}\n\n"
                    }
                }
            }
        }
    })
async def chat(
    payload: LLMRequest, 
    chat_service: ChatService = Depends(get_chat_service)
) -> Union[LLMResponse, StreamingResponse]:
    
    try:
        if payload.stream:
            return StreamingResponse(
                chat_service.stream_chat(payload), 
                media_type="text/event-stream"
            )
        else:
            return await chat_service.chat(payload)
    except Exception as e:
        raise APIError(detail=str(e))


