from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from app.core.config import settings
from app.core.logging import get_logger
from app.models.document import Document
from app.services.embedding_service import embedding_service
from app.services.pdf_service import pdf_service
from app.services.text_chunker import text_chunker
from app.services.text_extractor import text_extractor
from app.services.vector_store import vector_store
from app.utils.file_utils import (
    ensure_directory,
    generate_document_id,
    sanitize_filename,
)
from app.utils.validation import (
    validate_file_extension,
    validate_file_size,
)

logger = get_logger(__name__)


class DocumentService:
    """Manage PDF documents and their RAG ingestion lifecycle."""

    def __init__(self) -> None:
        self.upload_directory = ensure_directory(
            settings.UPLOAD_DIRECTORY
        )
        self.processed_directory = ensure_directory(
            settings.PROCESSED_DIRECTORY
        )

        self._documents: dict[str, Document] = {}
        self._lock = Lock()

    def create_document(
        self,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> Document:
        if not filename:
            raise ValueError(
                "A filename is required."
            )

        if not validate_file_extension(
            filename,
            settings.ALLOWED_FILE_EXTENSIONS,
        ):
            raise ValueError(
                "Only PDF files are supported."
            )

        if not validate_file_size(
            size_bytes,
            settings.MAX_UPLOAD_SIZE_MB,
        ):
            raise ValueError(
                "The uploaded file exceeds the maximum "
                f"size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )

        document_id = generate_document_id()
        safe_filename = sanitize_filename(filename)

        document = Document(
            id=document_id,
            filename=safe_filename,
            content_type=content_type or "application/pdf",
            size_bytes=size_bytes,
            status="uploaded",
            created_at=datetime.now(timezone.utc),
        )

        with self._lock:
            self._documents[document_id] = document

        return document

    def get_document(
        self,
        document_id: str,
    ) -> Document | None:
        with self._lock:
            return self._documents.get(document_id)

    def list_documents(self) -> list[Document]:
        with self._lock:
            return sorted(
                self._documents.values(),
                key=lambda document: document.created_at,
                reverse=True,
            )

    def save_upload(
        self,
        document: Document,
        content: bytes,
    ) -> Path:
        if not content:
            raise ValueError(
                "The uploaded PDF is empty."
            )

        if not validate_file_size(
            len(content),
            settings.MAX_UPLOAD_SIZE_MB,
        ):
            raise ValueError(
                "The uploaded file exceeds the maximum "
                f"size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )

        path = (
            self.upload_directory
            / f"{document.id}_{document.filename}"
        )

        path.write_bytes(content)

        return path

    def ingest_document(
        self,
        document_id: str,
        file_path: Path,
    ) -> Document:
        document = self.get_document(document_id)

        if document is None:
            raise ValueError(
                "Document was not found."
            )

        try:
            document.status = "processing"

            extraction = text_extractor.extract(
                file_path=str(file_path),
                document_id=document.id,
            )

            if not extraction.pages:
                raise ValueError(
                    "No pages were found in the PDF."
                )

            if extraction.total_words == 0:
                raise ValueError(
                    "No extractable text was found in the PDF."
                )

            chunking = text_chunker.chunk_pages(
                pages=extraction.pages,
                filename=document.filename,
            )

            if not chunking.chunks:
                raise ValueError(
                    "The PDF could not be divided into "
                    "retrievable text chunks."
                )

            embeddings = embedding_service.embed_chunks(
                chunking.chunks
            )

            vector_store.add_chunks(
                chunks=chunking.chunks,
                embeddings=[
                    item.vector
                    for item in embeddings
                ],
            )

            document.page_count = extraction.page_count
            document.chunk_count = chunking.chunk_count
            document.status = "ready"

            processed_path = (
                self.processed_directory
                / f"{document.id}.txt"
            )

            processed_path.write_text(
                "\n\n".join(
                    page.text
                    for page in extraction.pages
                    if page.text
                ),
                encoding="utf-8",
            )

            logger.info(
                "Document %s is ready: %s pages, %s chunks.",
                document.id,
                document.page_count,
                document.chunk_count,
            )

            return document

        except Exception:
            document.status = "failed"

            logger.exception(
                "Document ingestion failed: %s",
                document.id,
            )

            raise

    def delete_document(
        self,
        document_id: str,
    ) -> bool:
        document = self.get_document(document_id)

        if document is None:
            return False

        vector_store.delete_document(
            document_id
        )

        upload_path = (
            self.upload_directory
            / f"{document.id}_{document.filename}"
        )

        processed_path = (
            self.processed_directory
            / f"{document.id}.txt"
        )

        upload_path.unlink(
            missing_ok=True
        )

        processed_path.unlink(
            missing_ok=True
        )

        with self._lock:
            self._documents.pop(
                document_id,
                None,
            )

        logger.info(
            "Document deleted: %s",
            document_id,
        )

        return True

    def count(self) -> int:
        with self._lock:
            return len(self._documents)


document_service = DocumentService()