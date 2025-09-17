import httpx
from app.core.config import settings
from typing import AsyncIterator, Optional, Dict

class OpenRouterClient:
    def __init__(self, *, timeout: float = 60) -> None:
        self.base = settings.openrouter_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}"
        }
        self._timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client
    
    async def chat(self, model_id: str, **kwargs: Dict) -> str:
        url = f"{self.base}/chat/completions"
        payload = {
            "model": model_id, 
            **kwargs
        }
        client = await self._get_client()
        r = await client.post(url, headers=self.headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    async def chat_stream(self, model_id: str, **kwargs: Dict) -> AsyncIterator[str]:
        url = f"{self.base}/chat/completions"
        payload = {
            "model": model_id,
            "stream": True,
            **kwargs
        }
        client = await self._get_client()
        async with client.stream("POST", url, headers=self.headers, json=payload) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if line.startswith("data: "):
                    data = line[len("data: "):]
                    if data == "[DONE]":
                        break
                    chunk = httpx.Response(200, content=data).json()
                    yield chunk["choices"][0]["delta"].get("content", "")   