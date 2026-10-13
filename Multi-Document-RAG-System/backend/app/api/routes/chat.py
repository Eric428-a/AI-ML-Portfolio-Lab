from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import verify_api_key
from app.models.chat import ChatConversation, ChatMessage
from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    ConversationListResponse,
    ConversationResponse,
    MessageResponse,
    RenameConversationRequest,
)
from app.services.rag.pipeline import get_rag_pipeline

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_rag_pipeline().answer(payload, db)
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if "not found" in message.lower() else 400
        raise HTTPException(status_code=status_code, detail=message) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail="The answer-generation service failed. Check the backend configuration.",
        ) from exc


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    total_result = await db.execute(
        select(func.count(ChatConversation.id))
    )
    total = total_result.scalar_one()

    result = await db.execute(
        select(ChatConversation)
        .order_by(ChatConversation.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    conversations = result.scalars().all()

    items = [
        ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            collection_id=conversation.collection_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[],
        )
        for conversation in conversations
    ]

    return ConversationListResponse(items=items, total=total)


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatConversation).where(
            ChatConversation.id == conversation_id
        )
    )
    conversation = result.scalar_one_or_none()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    message_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at)
    )
    messages = message_result.scalars().all()

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        collection_id=conversation.collection_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[
            MessageResponse(
                id=message.id,
                conversation_id=message.conversation_id,
                role=message.role,
                content=message.content,
                citations=message.citations or [],
                created_at=message.created_at,
            )
            for message in messages
        ],
    )


@router.patch(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse,
)
async def rename_conversation(
    conversation_id: str,
    payload: RenameConversationRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatConversation).where(
            ChatConversation.id == conversation_id
        )
    )
    conversation = result.scalar_one_or_none()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    conversation.title = payload.title.strip()
    await db.commit()
    await db.refresh(conversation)

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        collection_id=conversation.collection_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[],
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatConversation).where(
            ChatConversation.id == conversation_id
        )
    )
    conversation = result.scalar_one_or_none()

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    await db.delete(conversation)
    await db.commit()

    return {
        "success": True,
        "message": "Conversation deleted.",
        "conversation_id": conversation_id,
    }