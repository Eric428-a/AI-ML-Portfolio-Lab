from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.models.document import DocumentPage
from app.services.pdf_service import PDFService


def test_validate_pdf_rejects_missing_file() -> None:
    service = PDFService()

    with pytest.raises(FileNotFoundError):
        service.validate_pdf(
            Path("does-not-exist.pdf")
        )


def test_validate_pdf_rejects_non_pdf() -> None:
    service = PDFService()

    path = Path("document.txt")

    with pytest.raises(ValueError):
        service.validate_pdf(path)


def test_get_page_count_uses_reader(monkeypatch) -> None:
    service = PDFService()

    fake_reader = MagicMock()
    fake_reader.pages = [MagicMock(), MagicMock()]

    monkeypatch.setattr(
        "app.services.pdf_service.PdfReader",
        lambda _: fake_reader,
    )

    assert service.get_page_count("document.pdf") == 2


def test_extract_pages_preserves_page_numbers(
    monkeypatch,
) -> None:
    service = PDFService()

    first_page = MagicMock()
    first_page.extract_text.return_value = (
        "First page content."
    )

    second_page = MagicMock()
    second_page.extract_text.return_value = (
        "Second page content."
    )

    fake_reader = MagicMock()
    fake_reader.pages = [
        first_page,
        second_page,
    ]

    monkeypatch.setattr(
        "app.services.pdf_service.PdfReader",
        lambda _: fake_reader,
    )

    pages = service.extract_pages(
        file_path="document.pdf",
        document_id="doc-1",
    )

    assert len(pages) == 2
    assert isinstance(pages[0], DocumentPage)
    assert pages[0].page_number == 1
    assert pages[1].page_number == 2
    assert pages[0].document_id == "doc-1"