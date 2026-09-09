from unittest.mock import MagicMock

from app.models.chunk import RetrievedChunk
from app.services.retrieval_service import RetrievalService


def test_retrieval_filters_low_relevance_chunks() -> None:
    embedding_service = MagicMock()
    vector_store = MagicMock()

    embedding_service.embed_query.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    vector_store.query.return_value = [
        RetrievedChunk(
            chunk_id="high",
            document_id="doc",
            filename="file.pdf",
            page_number=1,
            text="Relevant content.",
            relevance_score=0.9,
        ),
        RetrievedChunk(
            chunk_id="low",
            document_id="doc",
            filename="file.pdf",
            page_number=2,
            text="Weak content.",
            relevance_score=0.1,
        ),
    ]

    service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    result = service.retrieve(
        query="What is relevant?"
    )

    assert result.count == 1
    assert result.chunks[0].chunk_id == "high"


def test_retrieval_passes_document_filter() -> None:
    embedding_service = MagicMock()
    vector_store = MagicMock()

    embedding_service.embed_query.return_value = [
        0.1,
        0.2,
    ]

    vector_store.query.return_value = []

    service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    service.retrieve(
        query="Question",
        top_k=3,
        document_id="document-123",
    )

    vector_store.query.assert_called_once_with(
        embedding=[0.1, 0.2],
        top_k=3,
        document_id="document-123",
    )