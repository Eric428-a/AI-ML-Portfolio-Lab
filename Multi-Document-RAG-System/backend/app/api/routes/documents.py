from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import verify_api_key
from app.schemas.document_schema import (
    DocumentChunkResponse,
    DocumentListResponse,
    DocumentResponse,
    DocumentUpdateRequest,
    DocumentUploadResponse,
)
from app.services.document_service import get_document_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_documents(
    files: list[UploadFile] = File(...),
    collection_id: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    service = get_document_service()
    documents = await service.upload_documents(
        files=files,
        db=db,
        collection_id=collection_id,
    )

    successful = sum(document.status == "ready" for document in documents)

    return DocumentUploadResponse(
        items=[DocumentResponse.model_validate(doc) for doc in documents],
        accepted=successful,
        failed=len(documents) - successful,
    )


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    collection_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    documents, total = await get_document_service().list_documents(
        db=db,
        page=page,
        page_size=page_size,
        collection_id=collection_id,
        status=status,
    )

    return DocumentListResponse(
        items=[DocumentResponse.model_validate(doc) for doc in documents],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    document = await get_document_service().get_document(document_id, db)
    return DocumentResponse.model_validate(document)


@router.get("/{document_id}/chunks", response_model=list[DocumentChunkResponse])
async def get_document_chunks(
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    chunks = await get_document_service().get_document_chunks(
        document_id,
        db,
    )
    return [
        DocumentChunkResponse.model_validate(chunk)
        for chunk in chunks
    ]


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    payload: DocumentUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    document = await get_document_service().update_document(
        document_id=document_id,
        db=db,
        filename=payload.filename,
        collection_id=payload.collection_id,
        metadata_json=payload.metadata_json,
    )
    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    await get_document_service().delete_document(document_id, db)

    return {
        "success": True,
        "message": "Document deleted successfully.",
        "document_id": document_id,
    }