from functools import lru_cache

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import EmbeddingResult
from app.models.document import DocumentChunk

logger = get_logger(__name__)


class EmbeddingService:
    """Generate semantic embeddings for document chunks and queries."""

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        self.model_name = (
            model_name
            or settings.EMBEDDING_MODEL
        )

        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import (
                    SentenceTransformer,
                )

                logger.info(
                    "Loading embedding model: %s",
                    self.model_name,
                )

                self._model = SentenceTransformer(
                    self.model_name
                )

            except Exception as exc:
                logger.exception(
                    "Unable to load embedding model."
                )

                raise RuntimeError(
                    "Embedding model could not be loaded."
                ) from exc

        return self._model

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return [
            embedding.tolist()
            for embedding in embeddings
        ]

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        embeddings = self.embed_texts([query])

        return embeddings[0]

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingResult]:
        if not chunks:
            return []

        vectors = self.embed_texts(
            [chunk.text for chunk in chunks]
        )

        return [
            EmbeddingResult(
                chunk_id=chunk.id,
                vector=vector,
            )
            for chunk, vector in zip(
                chunks,
                vectors,
                strict=True,
            )
        ]

    def dimension(self) -> int:
        return int(
            self.model.get_sentence_embedding_dimension()
        )


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


embedding_service = get_embedding_service()