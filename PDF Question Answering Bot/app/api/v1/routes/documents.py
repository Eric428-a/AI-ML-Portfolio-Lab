from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.core.config import settings
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
    DocumentStatus,
)
from app.schemas.response import DeleteResponse
from app.services.document_service import document_service

router = APIRouter()


def _to_response(document) -> DocumentResponse:
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        content_type=document.content_type,
        size_bytes=document.size_bytes,
        page_count=document.page_count,
        chunk_count=document.chunk_count,
        status=DocumentStatus(document.status),
        created_at=document.created_at,
    )


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are supported.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty.",
        )

    if len(content) > (
        settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    ):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                "The uploaded file exceeds the maximum "
                f"size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            ),
        )

    try:
        document = document_service.create_document(
            filename=file.filename,
            content_type=file.content_type
            or "application/pdf",
            size_bytes=len(content),
        )

        path = document_service.save_upload(
            document=document,
            content=content,
        )

        document_service.ingest_document(
            document_id=document.id,
            file_path=path,
        )

        return _to_response(document)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF processing failed.",
        ) from exc


@router.get(
    "",
    response_model=DocumentListResponse,
)
async def list_documents() -> DocumentListResponse:
    documents = document_service.list_documents()

    return DocumentListResponse(
        documents=[
            _to_response(document)
            for document in documents
        ],
        total=len(documents),
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: str,
) -> DocumentResponse:
    document = document_service.get_document(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return _to_response(document)


@router.delete(
    "/{document_id}",
    response_model=DeleteResponse,
)
async def delete_document(
    document_id: str,
) -> DeleteResponse:
    deleted = document_service.delete_document(
        document_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return DeleteResponse(
        success=True,
        message="Document deleted successfully.",
        deleted_id=document_id,
    )