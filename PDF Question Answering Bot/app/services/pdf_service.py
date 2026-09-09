from pathlib import Path

from pypdf import PdfReader

from app.core.logging import get_logger
from app.models.document import DocumentPage
from app.utils.text_utils import clean_text

logger = get_logger(__name__)


class PDFService:
    """Extract structured page text from PDF documents."""

    def validate_pdf(self, file_path: str | Path) -> bool:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file does not exist: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"PDF path is not a file: {path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF documents are supported."
            )

        return True

    def get_page_count(self, file_path: str | Path) -> int:
        self.validate_pdf(file_path)

        reader = PdfReader(str(file_path))

        return len(reader.pages)

    def extract_pages(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> list[DocumentPage]:
        self.validate_pdf(file_path)

        logger.info(
            "Extracting PDF text: %s",
            file_path,
        )

        reader = PdfReader(str(file_path))
        pages: list[DocumentPage] = []

        for index, page in enumerate(reader.pages, start=1):
            try:
                raw_text = page.extract_text() or ""
                text = clean_text(raw_text)

                pages.append(
                    DocumentPage(
                        document_id=document_id,
                        page_number=index,
                        text=text,
                    )
                )

            except Exception:
                logger.exception(
                    "Failed extracting page %s from %s",
                    index,
                    file_path,
                )

                pages.append(
                    DocumentPage(
                        document_id=document_id,
                        page_number=index,
                        text="",
                    )
                )

        logger.info(
            "Extracted %s pages from %s",
            len(pages),
            file_path,
        )

        return pages

    def extract_text(
        self,
        file_path: str | Path,
    ) -> str:
        self.validate_pdf(file_path)

        reader = PdfReader(str(file_path))
        extracted_pages: list[str] = []

        for page in reader.pages:
            text = clean_text(
                page.extract_text() or ""
            )

            if text:
                extracted_pages.append(text)

        return "\n\n".join(extracted_pages)


pdf_service = PDFService()