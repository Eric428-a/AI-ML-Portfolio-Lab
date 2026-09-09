from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True

    PROJECT_NAME: str = "PDF Question Answering Bot"
    PROJECT_DESCRIPTION: str = (
        "Production-ready RAG system for asking questions about PDF documents"
    )
    VERSION: str = "1.0.0"

    API_V1_PREFIX: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_FILE_EXTENSIONS: list[str] = [".pdf"]

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150
    TOP_K: int = 5
    MIN_RELEVANCE_SCORE: float = 0.25

    EMBEDDING_PROVIDER: str = "sentence-transformers"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    LLM_PROVIDER: str = "groq"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_KEY: str | None = None

    VECTOR_STORE: str = "chroma"
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    CHROMA_COLLECTION_NAME: str = "pdf_documents"

    UPLOAD_DIRECTORY: str = "./data/uploads"
    PROCESSED_DIRECTORY: str = "./data/processed"

    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
    ]

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        if isinstance(value, str):
            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        return value  # type: ignore[return-value]

    @field_validator("ALLOWED_FILE_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, value: object) -> list[str]:
        if isinstance(value, str):
            values = [
                item.strip().lower()
                for item in value.split(",")
                if item.strip()
            ]
        elif isinstance(value, list):
            values = [str(item).strip().lower() for item in value]
        else:
            return [".pdf"]

        return [
            item if item.startswith(".") else f".{item}"
            for item in values
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()