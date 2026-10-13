import logging
from functools import lru_cache

from app.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Loaded embedding model: %s", settings.EMBEDDING_MODEL)
            return self._model

        except Exception as exc:
            logger.exception("Could not load embedding model")
            raise RuntimeError(
                f"Embedding model could not be loaded: {exc}"
            ) from exc

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        model = self._load_model()

        vectors = model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_documents([text])
        return vectors[0]


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()