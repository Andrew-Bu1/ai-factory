import httpx
import time
from typing import Any, AsyncGenerator
from .base import BaseModel
import logging

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
        self._logger = logging.getLogger(__name__)

    def infer(
        self, 
        payload: dict[str, Any],
    ):
        """Generate text completion using OpenRouter.
    
        Returns:
            AsyncGenerator for streaming or Coroutine for non-streaming
        """        
        stream = payload.get("stream", False)
        if stream:
            # Return the async generator for streaming
            return self._stream_completion(payload)
        else:
            # Return the coroutine for non-streaming
            return self._complete(payload)
    
    async def _complete(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Make a non-streaming completion request.
        
        Args:
            payload: Request payload
            
        Returns:
            Full response from OpenRouter
        """
        start = time.time()

        try:
            response = await self._client.post("chat/completions", json=payload)

            self._logger.info(f"[LLM] HTTP {response.status_code} in {time.time() - start:.2f}s")

            response.raise_for_status()

            data = response.json()
            return data

        except httpx.HTTPError as e:
            self._logger.error(f"[LLM] HTTP error: {e} | Response text: {e.response.text if e.response else 'no response'}")
            raise

        except Exception as e:
            self._logger.error(f"[LLM] Unexpected error: {e}")
            raise

    
    async def _stream_completion(self, payload: dict[str, Any]) -> AsyncGenerator[str, None]:
        """Make a streaming completion request.
        
        Args:
            payload: Request payload
            
        Yields:
            Text chunks as they arrive
        """
        start = time.time()
        async with self._client.stream("POST", "/chat/completions", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                yield line

        self._logger.info(f"[LLM] Stream ended in {time.time() - start:.2f}s")



    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
