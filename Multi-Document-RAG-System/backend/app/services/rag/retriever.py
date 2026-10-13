from app.config import settings
from app.services.rag.reranker import rerank_results
from app.services.rag.vector_store import get_vector_store


class DocumentRetriever:
    def __init__(self):
        self.vector_store = get_vector_store()

    def retrieve(
        self,
        query: str,
        collection_id: str | None = None,
        document_ids: list[str] | None = None,
        top_k: int | None = None,
    ) -> list[dict]:
        limit = top_k or settings.RETRIEVAL_TOP_K

        candidates = self.vector_store.search(
            query=query,
            top_k=min(limit * 3, 60),
            collection_id=collection_id,
            document_ids=document_ids,
        )

        reranked = rerank_results(
            query=query,
            results=candidates,
            limit=limit,
        )

        threshold = settings.MIN_RELEVANCE_SCORE

        return [
            result
            for result in reranked
            if result["score"] >= threshold
        ]


def get_retriever() -> DocumentRetriever:
    return DocumentRetriever()