from dataclasses import dataclass

from app.core.logging import get_logger
from app.models.document import DocumentPage
from app.services.pdf_service import PDFService
from app.utils.text_utils import clean_text

logger = get_logger(__name__)


@dataclass(slots=True)
class ExtractionResult:
    document_id: str
    page_count: int
    pages: list[DocumentPage]
    total_characters: int
    total_words: int


class TextExtractor:
    """Convert PDF files into cleaned page-level text."""

    def __init__(self, pdf_service: PDFService) -> None:
        self.pdf_service = pdf_service

    def extract(
        self,
        file_path: str,
        document_id: str,
    ) -> ExtractionResult:
        pages = self.pdf_service.extract_pages(
            file_path=file_path,
            document_id=document_id,
        )

        total_characters = 0
        total_words = 0

        for page in pages:
            page.text = clean_text(page.text)

            total_characters += len(page.text)
            total_words += len(page.text.split())

        result = ExtractionResult(
            document_id=document_id,
            page_count=len(pages),
            pages=pages,
            total_characters=total_characters,
            total_words=total_words,
        )

        logger.info(
            "Document %s extracted: %s pages, %s words",
            document_id,
            result.page_count,
            result.total_words,
        )

        return result


text_extractor = TextExtractor(pdf_service)