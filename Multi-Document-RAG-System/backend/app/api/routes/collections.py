from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import verify_api_key
from app.models.collection import Collection
from app.models.document import Document
from app.schemas.collection_schema import (
    CollectionCreate,
    CollectionListResponse,
    CollectionResponse,
    CollectionUpdate,
)
from app.services.rag.vector_store import get_vector_store

router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
    dependencies=[Depends(verify_api_key)],
)


async def serialize_collection(
    collection: Collection,
    db: AsyncSession,
) -> CollectionResponse:
    count_result = await db.execute(
        select(func.count(Document.id)).where(
            Document.collection_id == collection.id
        )
    )

    return CollectionResponse(
        id=collection.id,
        name=collection.name,
        description=collection.description,
        created_at=collection.created_at,
        document_count=count_result.scalar_one(),
    )


@router.post("", response_model=CollectionResponse, status_code=201)
async def create_collection(
    payload: CollectionCreate,
    db: AsyncSession = Depends(get_db),
):
    name = payload.name.strip()

    existing = await db.execute(
        select(Collection).where(func.lower(Collection.name) == name.lower())
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="A collection with this name already exists.",
        )

    collection = Collection(
        name=name,
        description=payload.description,
    )

    db.add(collection)
    await db.commit()
    await db.refresh(collection)

    return await serialize_collection(collection, db)


@router.get("", response_model=CollectionListResponse)
async def list_collections(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    total_result = await db.execute(
        select(func.count(Collection.id))
    )
    total = total_result.scalar_one()

    result = await db.execute(
        select(Collection)
        .order_by(Collection.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    collections = result.scalars().all()

    items = [
        await serialize_collection(collection, db)
        for collection in collections
    ]

    return CollectionListResponse(items=items, total=total)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Collection).where(Collection.id == collection_id)
    )
    collection = result.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found.")

    return await serialize_collection(collection, db)


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_id: str,
    payload: CollectionUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Collection).where(Collection.id == collection_id)
    )
    collection = result.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found.")

    changes = payload.model_dump(exclude_unset=True)

    if "name" in changes and changes["name"] is not None:
        name = changes["name"].strip()

        duplicate = await db.execute(
            select(Collection).where(
                func.lower(Collection.name) == name.lower(),
                Collection.id != collection_id,
            )
        )

        if duplicate.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="A collection with this name already exists.",
            )

        collection.name = name

    if "description" in changes:
        collection.description = changes["description"]

    await db.commit()
    await db.refresh(collection)

    return await serialize_collection(collection, db)


@router.delete("/{collection_id}")
async def delete_collection(
    collection_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Collection).where(Collection.id == collection_id)
    )
    collection = result.scalar_one_or_none()

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found.")

    documents_result = await db.execute(
        select(Document).where(Document.collection_id == collection_id)
    )
    documents = documents_result.scalars().all()

    vector_store = get_vector_store()

    for document in documents:
        vector_store.delete_document(document.id, document.collection_id)

    await db.delete(collection)
    await db.commit()

    return {
        "success": True,
        "message": "Collection and its documents deleted.",
        "collection_id": collection_id,
        "deleted_documents": len(documents),
    }