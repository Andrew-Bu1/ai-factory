from collections.abc import AsyncGenerator
import httpx
import logging
from pydantic import BaseModel


class ChatService:
    def __init__(self, base_url: str, api_key: str):
        self.base_url: str = base_url
        self.api_key: str = api_key
        self._logger: logging.Logger = logging.getLogger(__name__)

    async def stream_chat(self, payload: BaseModel) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload.model_dump(),
                headers=headers,
            ) as response:
                try:
                    _ = response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    self._logger.error(
                        f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                    )
                    raise e
                async for line in response.aiter_lines():
                    if line:
                        yield line

    async def chat(self, payload: BaseModel) -> dict[str, str | int]:
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                try:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        json=payload.model_dump(),
                        headers=headers,
                    )
                    _ = response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as e:
                    self._logger.error(
                        f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                    )
                    raise e
        except Exception as e:
            self._logger.error(f"An error occurred: {str(e)}")
            raise e
