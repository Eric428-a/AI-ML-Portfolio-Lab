from pathlib import Path

from app.models.document import DocumentPage
from app.services.text_extractor import ExtractionResult


def test_extraction_result_defaults() -> None:
    result = ExtractionResult(
        document_id="doc-1",
        page_count=2,
        pages=[
            DocumentPage(
                document_id="doc-1",
                page_number=1,
                text="Hello world.",
            ),
            DocumentPage(
                document_id="doc-1",
                page_number=2,
                text="Second page.",
            ),
        ],
        total_characters=25,
        total_words=4,
    )

    assert result.document_id == "doc-1"
    assert result.page_count == 2
    assert len(result.pages) == 2
    assert result.total_words == 4


def test_document_page_metadata() -> None:
    page = DocumentPage(
        document_id="abc",
        page_number=3,
        text="Example PDF text.",
    )

    assert page.document_id == "abc"
    assert page.page_number == 3
    assert page.text == "Example PDF text."