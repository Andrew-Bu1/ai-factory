import httpx
import asyncio
from typing import Any, AsyncGenerator
from .base import BaseModel


class LLMModel(BaseModel):
    """AI model for text generation using OpenRouter API."""
    
    def __init__(
        self, 
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: int = 60
    ):
        """Initialize LLM model with OpenRouter configuration.
        
        Args:
            api_key: OpenRouter API key
            base_url: OpenRouter API base URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )

    async def infer(
        self, 
        payload: dict[str, Any],
    ) -> str | dict[str, Any]:
        """Generate text completion using OpenRouter.
    
        Returns:
            Generated text or full response dict if stream=False
        """        
        stream = payload.get("stream", False)
        if stream:
            return await self._stream_completion(payload)
        else:
            return await self._complete(payload)
    
    async def _complete(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Make a non-streaming completion request.
        
        Args:
            payload: Request payload
            
        Returns:
            Full response from OpenRouter
        """
        response = await self._client.post("/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def _stream_completion(self, payload: dict[str, Any]) -> AsyncGenerator[str, None]:
        """Make a streaming completion request.
        
        Args:
            payload: Request payload
            
        Yields:
            Text chunks as they arrive
        """
        async with self._client.stream("POST", "/chat/completions", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]  # Remove "data: " prefix
                    if data.strip() == "[DONE]":
                        break
                    try:
                        import json
                        chunk = json.loads(data)
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue
    
    def get_model_info(self) -> dict[str, Any]:
        """Get information about the LLM service.
        
        Returns:
            Dictionary containing service metadata
        """
        return {
            "type": "llm",
            "provider": "openrouter",
            "base_url": self.base_url,
            "timeout": self.timeout,
            "has_api_key": bool(self.api_key)
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
