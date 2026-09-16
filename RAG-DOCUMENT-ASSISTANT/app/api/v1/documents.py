from fastapi import APIRouter, File, UploadFile, status

from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
)
from app.services.document_service import document_service

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentResponse:
    return await document_service.upload(file)


@router.get(
    "",
    response_model=DocumentListResponse,
)
async def list_documents() -> DocumentListResponse:
    return await document_service.list_documents()