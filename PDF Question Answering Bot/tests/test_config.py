# tests/test_config.py

from app.core.config import Settings


def test_default_settings():
    settings = Settings()

    assert settings.PROJECT_NAME == "PDF Question Answering Bot"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.EMBEDDING_PROVIDER == "sentence-transformers"
    assert settings.VECTOR_STORE == "chroma"


def test_extension_parser():
    settings = Settings(
        ALLOWED_FILE_EXTENSIONS="pdf,.PDF"
    )

    assert settings.ALLOWED_FILE_EXTENSIONS == [".pdf", ".pdf"]


def test_cors_parser():
    settings = Settings(
        CORS_ORIGINS="http://localhost:8000, http://localhost:3000"
    )

    assert settings.CORS_ORIGINS == [
        "http://localhost:8000",
        "http://localhost:3000",
    ]