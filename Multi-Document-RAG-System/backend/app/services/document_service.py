import asyncio
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.collection import Collection
from app.models.document import Document, DocumentChunk
from app.services.chunking import split_text
from app.services.file_parser import extract_document_text, read_upload, validate_file_extension
from app.services.metadata_service import build_document_metadata
from app.services.rag.vector_store import get_vector_store
from app.utils.file_utils import (
    calculate_sha256,
    ensure_within_directory,
    make_storage_filename,
    safe_filename,
)
from app.utils.text_utils import normalize_text

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        self.vector_store = get_vector_store()

    async def upload_documents(
        self,
        files: list[UploadFile],
        db: AsyncSession,
        collection_id: str | None = None,
    ) -> list[Document]:
        if not files:
            raise HTTPException(status_code=400, detail="No files were provided.")

        if len(files) > settings.MAX_FILES_PER_UPLOAD:
            raise HTTPException(
                status_code=400,
                detail=f"Upload a maximum of {settings.MAX_FILES_PER_UPLOAD} files per request.",
            )

        if collection_id:
            result = await db.execute(
                select(Collection).where(Collection.id == collection_id)
            )
            if result.scalar_one_or_none() is None:
                raise HTTPException(status_code=404, detail="Collection not found.")

        saved_documents = []
        max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

        for upload in files:
            original_filename = safe_filename(upload.filename or "document.txt")
            extension = validate_file_extension(original_filename)

            data = await read_upload(upload, max_size)
            checksum = calculate_sha256(data)

            existing_result = await db.execute(
                select(Document).where(
                    Document.checksum == checksum,
                    Document.collection_id == collection_id,
                )
            )
            existing = existing_result.scalar_one_or_none()

            if existing:
                raise HTTPException(
                    status_code=409,
                    detail=f"Duplicate file already exists: {original_filename}",
                )

            stored_filename = make_storage_filename(original_filename)
            stored_path = ensure_within_directory(
                settings.UPLOAD_DIR / stored_filename,
                settings.UPLOAD_DIR,
            )

            stored_path.parent.mkdir(parents=True, exist_ok=True)
            stored_path.write_bytes(data)

            document = Document(
                id=str(uuid4()),
                filename=stored_filename,
                original_filename=original_filename,
                content_type=upload.content_type or "application/octet-stream",
                file_size=len(data),
                checksum=checksum,
                storage_path=str(stored_path),
                status="processing",
                collection_id=collection_id,
                metadata_json=build_document_metadata(
                    filename=original_filename,
                    content_type=upload.content_type or "application/octet-stream",
                    file_size=len(data),
                    checksum=checksum,
                ),
            )

            db.add(document)
            await db.flush()

            try:
                await self._process_document(document, data, db)
                saved_documents.append(document)

            except Exception as exc:
                logger.exception("Document ingestion failed: %s", original_filename)
                document.status = "failed"
                document.error_message = str(exc)[:2000]
                saved_documents.append(document)

        await db.commit()

        for document in saved_documents:
            await db.refresh(document)

        return saved_documents

    async def _process_document(
        self,
        document: Document,
        data: bytes,
        db: AsyncSession,
    ) -> None:
        text, segments = await asyncio.to_thread(
            extract_document_text,
            document.original_filename,
            data,
        )

        text = normalize_text(text)

        chunks = split_text(
            text=text,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            base_metadata={
                "document_id": document.id,
                "filename": document.original_filename,
            },
        )

        if not chunks:
            raise ValueError("The document did not produce any text chunks.")

        chunk_rows = []

        for chunk in chunks:
            chunk_metadata = dict(chunk.metadata)

            if segments and document.original_filename.lower().endswith(".pdf"):
                page = self._find_pdf_page(chunk.text, segments)
                if page is not None:
                    chunk_metadata["page"] = page

            row = DocumentChunk(
                id=str(uuid4()),
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                metadata_json=chunk_metadata,
            )

            db.add(row)
            chunk_rows.append(row)

        await db.flush()

        vector_payload = [
            {
                "id": row.id,
                "chunk_index": row.chunk_index,
                "text": row.text,
                "metadata_json": row.metadata_json,
            }
            for row in chunk_rows
        ]

        await asyncio.to_thread(
            self.vector_store.add_chunks,
            document.id,
            document.original_filename,
            vector_payload,
            document.collection_id,
        )

        document.chunk_count = len(chunk_rows)
        document.status = "ready"
        document.error_message = None
        document.metadata_json = {
            **(document.metadata_json or {}),
            "character_count": len(text),
            "segment_count": len(segments),
        }

    @staticmethod
    def _find_pdf_page(text: str, pages: list[dict]) -> int | None:
        normalized = normalize_text(text)

        for page in pages:
            page_text = normalize_text(page.get("text", ""))
            if normalized and normalized[:100] in page_text:
                return int(page["page"])

        return None

    async def list_documents(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        collection_id: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Document], int]:
        filters = []

        if collection_id:
            filters.append(Document.collection_id == collection_id)

        if status:
            filters.append(Document.status == status)

        count_result = await db.execute(
            select(func.count(Document.id)).where(*filters)
        )
        total = count_result.scalar_one()

        result = await db.execute(
            select(Document)
            .where(*filters)
            .order_by(Document.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return list(result.scalars().all()), total

    async def get_document(
        self,
        document_id: str,
        db: AsyncSession,
    ) -> Document:
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )

        document = result.scalar_one_or_none()

        if document is None:
            raise HTTPException(status_code=404, detail="Document not found.")

        return document

    async def get_document_chunks(
        self,
        document_id: str,
        db: AsyncSession,
    ) -> list[DocumentChunk]:
        await self.get_document(document_id, db)

        result = await db.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        return list(result.scalars().all())

    async def delete_document(
        self,
        document_id: str,
        db: AsyncSession,
    ) -> None:
        document = await self.get_document(document_id, db)

        try:
            await asyncio.to_thread(
                self.vector_store.delete_document,
                document.id,
                document.collection_id,
            )
        except Exception:
            logger.exception("Vector deletion failed for %s", document_id)
            raise HTTPException(
                status_code=500,
                detail="Could not remove document vectors.",
            )

        storage_path = Path(document.storage_path)

        await db.delete(document)
        await db.commit()

        try:
            safe_path = ensure_within_directory(
                storage_path,
                settings.UPLOAD_DIR,
            )
            if safe_path.is_file():
                safe_path.unlink()
        except (OSError, ValueError):
            logger.exception("Could not remove stored file for %s", document_id)

    async def update_document(
        self,
        document_id: str,
        db: AsyncSession,
        filename: str | None = None,
        collection_id: str | None = None,
        metadata_json: dict | None = None,
    ) -> Document:
        document = await self.get_document(document_id, db)

        if filename is not None:
            document.original_filename = safe_filename(filename)

        if collection_id is not None:
            collection_result = await db.execute(
                select(Collection).where(Collection.id == collection_id)
            )
            if collection_result.scalar_one_or_none() is None:
                raise HTTPException(status_code=404, detail="Collection not found.")

            raise HTTPException(
                status_code=409,
                detail="Moving documents between collections requires reindexing. Re-upload the document to the target collection.",
            )

        if metadata_json is not None:
            document.metadata_json = {
                **(document.metadata_json or {}),
                **metadata_json,
            }

        await db.commit()
        await db.refresh(document)

        return document


def get_document_service() -> DocumentService:
    return DocumentService()