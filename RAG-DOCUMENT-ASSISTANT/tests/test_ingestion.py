from pathlib import Path

from app.rag.chunker import chunk_text
from app.rag.loader import load_document


def test_chunk_text_returns_chunks():
    text = " ".join(
        ["document"] * 300
    )

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert chunks
    assert all(
        isinstance(chunk, str)
        for chunk in chunks
    )


def test_chunk_text_empty_text():
    result = chunk_text("")

    assert result == []


def test_load_txt_document(tmp_path):
    document = tmp_path / "sample.txt"

    document.write_text(
        "Hello from the RAG document.",
        encoding="utf-8",
    )

    result = load_document(document)

    assert result == (
        "Hello from the RAG document."
    )


def test_load_missing_document(tmp_path):
    document = (
        Path(tmp_path)
        / "missing.txt"
    )

    try:
        load_document(document)
        assert False
    except FileNotFoundError:
        assert True