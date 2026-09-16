from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG Document Assistant"
    app_version: str = "1.0.0"
    environment: str = "development"

    api_prefix: str = "/api/v1"

    host: str = "127.0.0.1"
    port: int = 8000

    log_level: str = "INFO"

    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://127.0.0.1:8000", "http://localhost:8000"]
    )

    upload_dir: str = "data/uploads"
    document_dir: str = "data/documents"
    processed_dir: str = "data/processed"

    max_upload_size_mb: int = 25

    database_url: str = "sqlite:///./data/rag_assistant.db"

    vector_store_path: str = "data/processed/vector_store"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""

    chunk_size: int = 800
    chunk_overlap: int = 120
    retrieval_top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()