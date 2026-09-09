from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import RetrievalResult, RetrievedChunk
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.utils.validation import validate_top_k

logger = get_logger(__name__)


class RetrievalService:
    """Retrieve the most relevant PDF chunks for a question."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        document_id: str | None = None,
    ) -> RetrievalResult:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        limit = top_k or settings.TOP_K

        validate_top_k(limit)

        query_embedding = (
            self.embedding_service.embed_query(query)
        )

        chunks = self.vector_store.query(
            embedding=query_embedding,
            top_k=limit,
            document_id=document_id,
        )

        filtered_chunks: list[RetrievedChunk] = [
            chunk
            for chunk in chunks
            if (
                chunk.relevance_score
                >= settings.MIN_RELEVANCE_SCORE
            )
        ]

        logger.info(
            "Retrieved %s relevant chunks for query.",
            len(filtered_chunks),
        )

        return RetrievalResult(
            query=query,
            chunks=filtered_chunks,
        )


retrieval_service = RetrievalService(
    embedding_service=__import__(
        "app.services.embedding_service",
        fromlist=["embedding_service"],
    ).embedding_service,
    vector_store=vector_store,
)