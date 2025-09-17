from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    app_name: str = "AI Factory"
    
    # OpenRouter settings
    openrouter_api_key: str = Field(default=os.getenv("OPENROUTER_API_KEY", ""))
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

settings = Settings()