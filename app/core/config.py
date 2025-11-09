from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "AI Factory"

    # OpenRouter settings
    openrouter_api_key: str = Field(default="sdfasdf", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL"
    )
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5431/ai_factory", alias="DATABASE_URL"
    )

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings: Settings = Settings()
