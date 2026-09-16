from app.core.config import settings
from app.rag.retriever import RetrievedChunk, retriever


class RetrievalService:
    def search(
        self,
        question: str,
        document_ids: list[int] | None = None,
        top_k: int | None = None,
    ) -> list[RetrievedChunk]:
        return retriever.search(
            question=question,
            document_ids=document_ids,
            top_k=top_k or settings.retrieval_top_k,
        )


retrieval_service = RetrievalService()