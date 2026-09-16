from app.rag.embeddings import embedding_model


class EmbeddingService:
    def embed_text(self, text: str) -> list[float]:
        return embedding_model.embed(text)

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return embedding_model.embed_many(texts)


embedding_service = EmbeddingService()