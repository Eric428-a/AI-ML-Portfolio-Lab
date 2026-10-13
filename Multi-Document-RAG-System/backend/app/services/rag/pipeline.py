from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.chat import ChatConversation, ChatMessage
from app.models.document import Document
from app.schemas.chat_schema import Citation, ChatRequest, ChatResponse
from app.services.llm_service import get_llm_service
from app.services.rag.prompts import SYSTEM_PROMPT, build_rag_prompt
from app.services.rag.retriever import get_retriever


class RAGPipeline:
    def __init__(self):
        self.retriever = get_retriever()
        self.llm = get_llm_service()

    async def answer(
        self,
        request: ChatRequest,
        db: AsyncSession,
    ) -> ChatResponse:
        question = request.question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        conversation = await self._get_or_create_conversation(
            request=request,
            db=db,
        )

        results = self.retriever.retrieve(
            query=question,
            collection_id=request.collection_id,
            document_ids=request.document_ids,
            top_k=request.top_k or settings.RETRIEVAL_TOP_K,
        )

        contexts = [
            {
                "chunk_id": result["chunk_id"],
                "filename": result["filename"],
                "chunk_index": result["chunk_index"],
                "text": result["text"],
            }
            for result in results
        ]

        user_prompt = build_rag_prompt(question, contexts)

        answer = await self._generate_answer(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        citations = []

        if request.include_sources:
            citations = [
                Citation(
                    document_id=result["document_id"],
                    filename=result["filename"],
                    chunk_id=result["chunk_id"],
                    chunk_index=int(result["chunk_index"]),
                    text=result["text"],
                    score=float(result.get("rerank_score", result["score"])),
                    page=result.get("metadata", {}).get("page"),
                )
                for result in results
            ]

        now = datetime.now(timezone.utc)

        user_message = ChatMessage(
            id=str(uuid4()),
            conversation_id=conversation.id,
            role="user",
            content=question,
            citations=[],
        )

        assistant_message = ChatMessage(
            id=str(uuid4()),
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
            citations=[citation.model_dump() for citation in citations],
            metadata_json={
                "model": settings.LLM_MODEL,
                "retrieved_chunks": len(results),
            },
        )

        conversation.updated_at = now

        await db.merge(conversation)
        db.add(user_message)
        db.add(assistant_message)

        await db.commit()

        return ChatResponse(
            answer=answer,
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            citations=citations,
            retrieved_chunks=len(results),
            model=settings.LLM_MODEL,
            created_at=now,
        )

    async def _generate_answer(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        import asyncio

        return await asyncio.to_thread(
            self.llm.generate,
            system_prompt,
            user_prompt,
        )

    async def _get_or_create_conversation(
        self,
        request: ChatRequest,
        db: AsyncSession,
    ) -> ChatConversation:
        if request.conversation_id:
            result = await db.execute(
                select(ChatConversation).where(
                    ChatConversation.id == request.conversation_id
                )
            )

            conversation = result.scalar_one_or_none()

            if conversation is None:
                raise ValueError("Conversation not found.")

            if (
                request.collection_id
                and conversation.collection_id
                and request.collection_id != conversation.collection_id
            ):
                raise ValueError(
                    "The conversation belongs to a different collection."
                )

            return conversation

        conversation = ChatConversation(
            id=str(uuid4()),
            title=request.question[:80].strip(),
            collection_id=request.collection_id,
        )

        db.add(conversation)
        await db.flush()

        return conversation


def get_rag_pipeline() -> RAGPipeline:
    return RAGPipeline()