from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.models.document import DocumentPage
from app.services.document_service import DocumentService


def test_create_document_rejects_non_pdf() -> None:
    service = DocumentService()

    with pytest.raises(ValueError):
        service.create_document(
            filename="document.txt",
            content_type="text/plain",
            size_bytes=100,
        )


def test_create_document_creates_document() -> None:
    service = DocumentService()

    document = service.create_document(
        filename="research.pdf",
        content_type="application/pdf",
        size_bytes=1024,
    )

    assert document.filename == "research.pdf"
    assert document.content_type == "application/pdf"
    assert document.size_bytes == 1024
    assert document.status == "uploaded"

    assert service.get_document(
        document.id
    ) is document


def test_list_documents_returns_created_documents() -> None:
    service = DocumentService()

    first = service.create_document(
        filename="first.pdf",
        content_type="application/pdf",
        size_bytes=100,
    )

    second = service.create_document(
        filename="second.pdf",
        content_type="application/pdf",
        size_bytes=200,
    )

    documents = service.list_documents()

    ids = {document.id for document in documents}

    assert first.id in ids
    assert second.id in ids
    assert len(documents) == 2


def test_save_upload_creates_file(
    tmp_path: Path,
) -> None:
    service = DocumentService()

    service.upload_directory = tmp_path

    document = service.create_document(
        filename="sample.pdf",
        content_type="application/pdf",
        size_bytes=5,
    )

    path = service.save_upload(
        document=document,
        content=b"12345",
    )

    assert path.exists()
    assert path.read_bytes() == b"12345"


def test_ingest_document_updates_metadata(
    tmp_path: Path,
    monkeypatch,
) -> None:
    service = DocumentService()

    service.processed_directory = tmp_path

    document = service.create_document(
        filename="research.pdf",
        content_type="application/pdf",
        size_bytes=100,
    )

    extraction = MagicMock()
    extraction.pages = [
        DocumentPage(
            document_id=document.id,
            page_number=1,
            text="Useful document content.",
        )
    ]
    extraction.page_count = 1
    extraction.total_words = 3

    chunk = MagicMock()
    chunking = MagicMock()
    chunking.chunks = [chunk]
    chunking.chunk_count = 1

    embedding = MagicMock()
    embedding.vector = [0.1, 0.2, 0.3]

    monkeypatch.setattr(
        "app.services.document_service.text_extractor.extract",
        lambda **kwargs: extraction,
    )

    monkeypatch.setattr(
        "app.services.document_service.text_chunker.chunk_pages",
        lambda **kwargs: chunking,
    )

    monkeypatch.setattr(
        "app.services.document_service.embedding_service.embed_chunks",
        lambda chunks: [embedding],
    )

    vector_store = MagicMock()

    monkeypatch.setattr(
        "app.services.document_service.vector_store",
        vector_store,
    )

    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"fake")

    result = service.ingest_document(
        document_id=document.id,
        file_path=pdf_path,
    )

    assert result.status == "ready"
    assert result.page_count == 1
    assert result.chunk_count == 1

    vector_store.add_chunks.assert_called_once()