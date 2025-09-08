import httpx
from app.core.config import settings

class OpenRouterClient:
    def __init__(self) -> None:
        self.base = settings.openrouter_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }

    async def chat(self, messages, model: str | None = None, **kwargs):
        url = f"{self.base}/chat/completions"
        payload = {"model": model or settings.openrouter_model, "messages": messages}
        payload.update(kwargs)

        async with httpx.AsyncClient() as client:
            r = await client.post(url, headers=self.headers, json=payload)

            data = r.json()
            return data["choices"][0]["message"]["content"]