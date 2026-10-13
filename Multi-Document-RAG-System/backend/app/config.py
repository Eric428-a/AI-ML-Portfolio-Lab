import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "Multi-Document RAG System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR / 'rag.db'}"

    STORAGE_DIR: Path = BASE_DIR / "app" / "storage"
    UPLOAD_DIR: Path = BASE_DIR / "app" / "storage" / "uploads"
    VECTOR_DB_DIR: Path = BASE_DIR / "app" / "storage" / "vector_db"

    MAX_UPLOAD_SIZE_MB: int = Field(default=25, ge=1, le=200)
    MAX_FILES_PER_UPLOAD: int = Field(default=20, ge=1, le=100)
    CHUNK_SIZE: int = Field(default=1000, ge=100, le=10000)
    CHUNK_OVERLAP: int = Field(default=150, ge=0, le=2000)
    RETRIEVAL_TOP_K: int = Field(default=5, ge=1, le=30)
    MIN_RELEVANCE_SCORE: float = Field(default=0.15, ge=0.0, le=1.0)

    VECTOR_STORE_PROVIDER: str = "chroma"
    EMBEDDING_PROVIDER: str = "sentence-transformers"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    LLM_PROVIDER: str = "groq"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""
    LLM_TEMPERATURE: float = Field(default=0.1, ge=0.0, le=2.0)
    LLM_MAX_TOKENS: int = Field(default=1200, ge=100, le=8000)
    LLM_TIMEOUT_SECONDS: float = Field(default=60.0, gt=0, le=300)

    API_KEY: str = ""
    REQUIRE_API_KEY: bool = False

    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [
                origin.strip().rstrip("/")
                for origin in value.split(",")
                if origin.strip()
            ]
        return value

    @field_validator("VECTOR_STORE_PROVIDER")
    @classmethod
    def validate_vector_provider(cls, value):
        value = value.lower().strip()
        if value not in {"chroma"}:
            raise ValueError("VECTOR_STORE_PROVIDER must be 'chroma'")
        return value

    @field_validator("LLM_PROVIDER")
    @classmethod
    def validate_llm_provider(cls, value):
        value = value.lower().strip()
        if value not in {"groq", "openai", "ollama", "none"}:
            raise ValueError(
                "LLM_PROVIDER must be groq, openai, ollama, or none"
            )
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

for directory in (
    settings.STORAGE_DIR,
    settings.UPLOAD_DIR,
    settings.VECTOR_DB_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)