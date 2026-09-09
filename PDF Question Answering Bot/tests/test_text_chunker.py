from app.models.document import DocumentPage
from app.services.text_chunker import TextChunker


def make_page(text: str) -> DocumentPage:
    return DocumentPage(
        document_id="document-123",
        page_number=1,
        text=text,
    )


def test_empty_page_produces_no_chunks() -> None:
    chunker = TextChunker(
        chunk_size=10,
        chunk_overlap=2,
    )

    result = chunker.chunk_pages(
        pages=[make_page("")],
        filename="test.pdf",
    )

    assert result.chunk_count == 0
    assert result.chunks == []


def test_chunker_creates_multiple_chunks() -> None:
    text = " ".join(
        f"word{i}"
        for i in range(25)
    )

    chunker = TextChunker(
        chunk_size=10,
        chunk_overlap=2,
    )

    result = chunker.chunk_pages(
        pages=[make_page(text)],
        filename="test.pdf",
    )

    assert result.chunk_count == 3
    assert result.chunks[0].page_number == 1
    assert result.chunks[0].chunk_index == 0
    assert result.chunks[1].chunk_index == 1


def test_chunk_overlap_is_applied() -> None:
    text = " ".join(
        f"word{i}"
        for i in range(12)
    )

    chunker = TextChunker(
        chunk_size=6,
        chunk_overlap=2,
    )

    result = chunker.chunk_pages(
        pages=[make_page(text)],
        filename="test.pdf",
    )

    first_words = result.chunks[0].text.split()
    second_words = result.chunks[1].text.split()

    assert first_words[-2:] == second_words[:2]


def test_page_metadata_is_preserved() -> None:
    page = DocumentPage(
        document_id="doc-1",
        page_number=7,
        text="This is a document page with useful content.",
    )

    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=10,
    )

    result = chunker.chunk_pages(
        pages=[page],
        filename="research.pdf",
    )

    assert len(result.chunks) == 1

    chunk = result.chunks[0]

    assert chunk.document_id == "doc-1"
    assert chunk.filename == "research.pdf"
    assert chunk.page_number == 7