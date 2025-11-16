from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from ..schemas.llm import (
    LLMRequest, 
    LLMResponse
)
from app.api.errors import (
    APIError
)
from app.api.deps import get_llm_model, LLMModel
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
    llm_model: LLMModel = Depends(get_llm_model)
) -> Union[LLMResponse, StreamingResponse]:
    
    try:
        payload_dict = payload.model_dump(exclude_none=True)

        if payload.stream:
            return StreamingResponse(
                llm_model.infer(payload_dict),
                media_type="text/event-stream"
            )
        
        return await llm_model.infer(payload_dict)
    except Exception as e:
        raise APIError(detail=str(e))


