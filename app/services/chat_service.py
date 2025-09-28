from typing import AsyncGenerator
import httpx
import logging
class ChatService:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self._logger = logging.getLogger(__name__)

    async def stream_chat(self, payload) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            async with client.stream("POST", f"{self.base_url}/chat/completions", json=payload.dict(), headers=headers) as response:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    self._logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                    raise e
                async for line in response.aiter_lines():
                    if line:
                        yield line  
            

    async def chat(self, payload) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                try:
                    response = await client.post(f"{self.base_url}/chat/completions", json=payload.dict(), headers=headers)
                    response.raise_for_status()
                    return response.json()  
                except httpx.HTTPStatusError as e:
                    self._logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                    raise e
        except Exception as e:
            self._logger.error(f"An error occurred: {str(e)}")
            raise e