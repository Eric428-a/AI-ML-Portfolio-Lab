import io

import pytest
from fastapi import HTTPException, UploadFile

from app.services.chunking import split_text
from app.services.file_parser import (
    extract_document_text,
    validate_file_extension,
)
from app.utils.file_utils import calculate_sha256, safe_filename


def test_supported_extensions():
    assert validate_file_extension("report.pdf") == ".pdf"
    assert validate_file_extension("report.docx") == ".docx"
    assert validate_file_extension("notes.txt") == ".txt"
    assert validate_file_extension("notes.md") == ".md"
    assert validate_file_extension("data.csv") == ".csv"


def test_reject_unsupported_extension():
    with pytest.raises(HTTPException) as exc:
        validate_file_extension("malware.exe")

    assert exc.value.status_code == 415


def test_text_extraction():
    text, segments = extract_document_text(
        "notes.txt",
        b"Multi-document retrieval augmented generation.",
    )

    assert "retrieval augmented generation" in text
    assert len(segments) == 1


def test_csv_extraction():
    text, _ = extract_document_text(
        "data.csv",
        b"name,department\nEric,Engineering\n",
    )

    assert "Engineering" in text
    assert "Eric" in text


def test_chunking():
    text = "A" * 2500

    chunks = split_text(
        text,
        chunk_size=500,
        chunk_overlap=100,
    )

    assert len(chunks) > 1
    assert all(chunk.text for chunk in chunks)
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_empty_text_returns_no_chunks():
    assert split_text("   ") == []


def test_chunk_overlap_validation():
    with pytest.raises(ValueError):
        split_text("example", chunk_size=100, chunk_overlap=100)


def test_file_hash_is_deterministic():
    content = b"document content"

    assert calculate_sha256(content) == calculate_sha256(content)


def test_safe_filename_removes_directory_components():
    assert safe_filename("../../document.txt") == "document.txt"


def test_empty_file_is_rejected_by_extractor():
    with pytest.raises(ValueError):
        extract_document_text("empty.txt", b"")