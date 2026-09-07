from functools import lru_cache

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    APP_NAME: str = "AI Text Summarizer"

    APP_DESCRIPTION: str = (
        "AI-powered text summarization API."
    )

    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
    )

    MAX_INPUT_CHARACTERS: int = 100_000

    DEFAULT_MAX_LENGTH: int = 150

    DEFAULT_MIN_LENGTH: int = 30

    MODEL_PROVIDER: str = "local"

    MODEL_NAME: str = (
        "extractive-summarizer-v1"
    )

    GROQ_API_KEY: str | None = None

    OPENAI_API_KEY: str | None = None

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()