from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    SourceReference,
)
from app.services.llm_service import llm_service
from app.services.retrieval_service import retrieval_service


class ChatService:
    async def answer(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        retrieved = retrieval_service.search(
            question=request.question,
            document_ids=request.document_ids,
            top_k=request.top_k,
        )

        contexts = [
            item.content
            for item in retrieved
        ]

        answer = llm_service.generate(
            question=request.question,
            contexts=contexts,
        )

        sources = [
            SourceReference(
                document_id=item.document_id,
                filename=item.filename,
                chunk_index=item.chunk_index,
                page_number=item.page_number,
                content=item.content,
            )
            for item in retrieved
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
        )


chat_service = ChatService()