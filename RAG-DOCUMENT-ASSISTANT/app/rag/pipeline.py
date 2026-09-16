from app.rag.prompt import build_rag_prompt
from app.rag.retriever import retriever


class RAGPipeline:
    def retrieve(
        self,
        question: str,
        document_ids: list[int] | None = None,
        top_k: int = 5,
    ):
        return retriever.search(
            question=question,
            document_ids=document_ids,
            top_k=top_k,
        )

    def build_prompt(
        self,
        question: str,
        contexts: list[str],
    ) -> str:
        return build_rag_prompt(
            question=question,
            contexts=contexts,
        )


rag_pipeline = RAGPipeline()