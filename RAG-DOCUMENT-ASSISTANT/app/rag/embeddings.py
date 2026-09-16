from app.core.config import settings


class EmbeddingModel:
    def __init__(self) -> None:
        self._model = None

    def _load(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(
                settings.embedding_model
            )

        return self._model

    def embed(self, text: str) -> list[float]:
        model = self._load()

        vector = model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        model = self._load()

        vectors = model.encode(
            texts,
            normalize_embeddings=True,
        )

        return [
            vector.tolist()
            for vector in vectors
        ]


embedding_model = EmbeddingModel()