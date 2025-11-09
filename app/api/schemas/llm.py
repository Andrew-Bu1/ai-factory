from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union


class FunctionDefinition(BaseModel):
    name: str = Field(..., example="get_current_weather")
    description: str = Field(..., example="Get the current weather in a given location")
    parameters: dict = Field(
        ...,
        example={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    )
    required: list[str] = Field(..., example=["location"])


class Tool(BaseModel):
    type: str = Field(
        "function",
        description="The type of the tool. Currently, only 'function' is supported.",
    )
    function: FunctionDefinition


class LLMRequest(BaseModel):
    model: str = Field(..., example="gpt-4o")
    messages: List[Dict[str, Any]] = Field(
        ...,
        example=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! How can you assist me today?"},
        ],
    )
    tools: Optional[List[Tool]] = Field(
        None,
        description="A list of tools (functions) that the model can use to enhance its responses.",
    )
    tool_choice: Optional[Union[str, List[str]]] = Field(
        None,
        description="Specify which tool(s) the model is allowed to use. Can be a single tool name or a list of tool names.",
        example="get_current_weather",
    )

    temperature: Optional[float] = Field(None, example=0.7)
    max_tokens: Optional[int] = Field(None, example=150)
    top_p: Optional[float] = Field(None, example=1.0)
    frequency_penalty: Optional[float] = Field(None, example=0.0)
    presence_penalty: Optional[float] = Field(None, example=0.0)
    stream: bool = Field(False, example=False)


class LLMResponse(BaseModel):
    id: str = Field(..., example="chatcmpl-123")
    object: str = Field(..., example="chat.completion")
    created: int = Field(..., example=1677652288)
    model: str = Field(..., example="gpt-4o")
    choices: List[Dict[str, Any]] = Field(
        ...,
        example=[
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I assist you today?",
                },
                "finish_reason": "stop",
            }
        ],
    )
    usage: Optional[Dict[str, Any]] = Field(
        None, example={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    )


class LLMStreamResponse(BaseModel):
    id: str = Field(..., example="chatcmpl-123")
    object: str = Field(..., example="chat.completion.chunk")
    created: int = Field(..., example=1677652288)
    model: str = Field(..., example="gpt-4o")
    choices: List[Dict[str, Any]] = Field(
        ...,
        example=[
            {
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": "Hello! How can I assist you today?",
                },
                "finish_reason": None,
            }
        ],
    )
