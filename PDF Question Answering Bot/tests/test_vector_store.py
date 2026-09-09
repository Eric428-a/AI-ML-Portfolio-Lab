from unittest.mock import MagicMock

import pytest

from app.models.document import DocumentChunk
from app.services.vector_store import VectorStore


def make_chunk() -> DocumentChunk:
    return DocumentChunk(
        id="chunk-1",
        document_id="doc-1",
        filename="test.pdf",
        page_number=1,
        text="Example document text.",
        chunk_index=0,
        metadata={
            "document_id": "doc-1",
            "filename": "test.pdf",
            "page_number": 1,
            "chunk_index": 0,
        },
    )


def test_add_chunks_rejects_mismatched_embeddings(
    tmp_path,
) -> None:
    store = VectorStore(
        persist_directory=str(tmp_path),
        collection_name="test_collection",
    )

    with pytest.raises(ValueError):
        store.add_chunks(
            chunks=[make_chunk()],
            embeddings=[],
        )


def test_add_empty_chunks_returns_zero(
    tmp_path,
) -> None:
    store = VectorStore(
        persist_directory=str(tmp_path),
        collection_name="empty_collection",
    )

    assert store.add_chunks(
        chunks=[],
        embeddings=[],
    ) == 0


def test_vector_store_count(
    tmp_path,
) -> None:
    store = VectorStore(
        persist_directory=str(tmp_path),
        collection_name="count_collection",
    )

    assert store.count() == 0


def test_query_converts_distance_to_relevance(
    tmp_path,
) -> None:
    store = VectorStore.__new__(
        VectorStore
    )

    collection = MagicMock()

    collection.query.return_value = {
        "ids": [["chunk-1"]],
        "documents": [["Relevant content"]],
        "metadatas": [[
            {
                "document_id": "doc-1",
                "filename": "test.pdf",
                "page_number": 3,
            }
        ]],
        "distances": [[0.1]],
    }

    store.collection = collection

    result = store.query(
        embedding=[0.1, 0.2],
        top_k=1,
    )

    assert len(result) == 1
    assert result[0].chunk_id == "chunk-1"
    assert result[0].page_number == 3
    assert result[0].relevance_score == 0.9