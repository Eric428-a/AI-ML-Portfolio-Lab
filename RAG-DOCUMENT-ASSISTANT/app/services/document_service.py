from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select

from app.core.config import settings
from app.core.security import safe_filename
from app.db.database import SessionLocal
from app.db.models import Document
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
)


class DocumentService:
    allowed_extensions = {
        ".pdf",
        ".txt",
        ".docx",
    }

    async def upload(
        self,
        file: UploadFile,
    ) -> DocumentResponse:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required.",
            )

        filename = safe_filename(file.filename)
        extension = Path(filename).suffix.lower()

        if extension not in self.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Unsupported file type. "
                    "Allowed types: PDF, TXT, DOCX."
                ),
            )

        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = upload_dir / filename

        if destination.exists():
            stem = destination.stem
            suffix = destination.suffix
            counter = 1

            while destination.exists():
                destination = upload_dir / (
                    f"{stem}_{counter}{suffix}"
                )
                counter += 1

        content = await file.read()

        max_size = settings.max_upload_size_mb * 1024 * 1024

        if len(content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    f"File exceeds the "
                    f"{settings.max_upload_size_mb} MB limit."
                ),
            )

        destination.write_bytes(content)

        db = SessionLocal()

        try:
            document = Document(
                filename=destination.name,
                file_path=str(destination),
                file_type=extension.lstrip("."),
                status="uploaded",
            )

            db.add(document)
            db.commit()
            db.refresh(document)

            return DocumentResponse.model_validate(document)

        finally:
            db.close()

    async def list_documents(self) -> DocumentListResponse:
        db = SessionLocal()

        try:
            documents = list(
                db.scalars(
                    select(Document).order_by(
                        Document.created_at.desc()
                    )
                )
            )

            return DocumentListResponse(
                documents=[
                    DocumentResponse.model_validate(document)
                    for document in documents
                ],
                total=len(documents),
            )

        finally:
            db.close()


document_service = DocumentService()