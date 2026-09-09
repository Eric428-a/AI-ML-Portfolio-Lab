from unittest.mock import MagicMock

from app.services.embedding_service import EmbeddingService


def test_embedding_service_can_be_initialized() -> None:
    service = EmbeddingService(
        model_name="test-model"
    )

    assert service.model_name == "test-model"
    assert service._model is None


def test_embed_texts_returns_empty_for_empty_input() -> None:
    service = EmbeddingService()

    assert service.embed_texts([]) == []


def test_embed_texts_uses_model() -> None:
    service = EmbeddingService()

    fake_model = MagicMock()

    fake_model.encode.return_value = [
        [0.1, 0.2],
        [0.3, 0.4],
    ]

    service._model = fake_model

    result = service.embed_texts(
        ["first text", "second text"]
    )

    assert result == [
        [0.1, 0.2],
        [0.3, 0.4],
    ]

    fake_model.encode.assert_called_once()