from pydantic_settings import BaseSettings
import os
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    app_name: str = "AI Factory"
    
    # OpenRouter settings
    openrouter_api_key: str = Field(..., alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(..., alias="OPENROUTER_BASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()