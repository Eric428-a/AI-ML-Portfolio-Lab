from dataclasses import dataclass

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import RetrievedChunk
from app.schemas.question import QuestionResponse, SourceReference
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService

logger = get_logger(__name__)


@dataclass(slots=True)
class QAContext:
    chunks: list[RetrievedChunk]

    def as_text(self) -> str:
        sections: list[str] = []

        for index, chunk in enumerate(
            self.chunks,
            start=1,
        ):
            sections.append(
                "\n".join(
                    [
                        f"[Source {index}]",
                        f"File: {chunk.filename}",
                        f"Page: {chunk.page_number}",
                        f"Content: {chunk.text}",
                    ]
                )
            )

        return "\n\n".join(sections)


class QAService:
    """Coordinate retrieval and grounded LLM generation."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def _build_sources(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[SourceReference]:
        return [
            SourceReference(
                document_id=chunk.document_id,
                filename=chunk.filename,
                page_number=chunk.page_number,
                chunk_id=chunk.chunk_id,
                relevance_score=round(
                    chunk.relevance_score,
                    4,
                ),
                excerpt=chunk.text[:500],
            )
            for chunk in chunks
        ]

    def ask(
        self,
        question: str,
        document_id: str | None = None,
        top_k: int | None = None,
    ) -> QuestionResponse:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        retrieval = self.retrieval_service.retrieve(
            query=question,
            top_k=top_k or settings.TOP_K,
            document_id=document_id,
        )

        context = QAContext(
            chunks=retrieval.chunks
        )

        if not retrieval.chunks:
            return QuestionResponse(
                question=question,
                answer=(
                    "I could not find enough relevant "
                    "information in the provided document "
                    "to answer this question."
                ),
                sources=[],
                model=self.llm_service.model,
                retrieval_count=0,
            )

        llm_response = self.llm_service.generate(
            question=question,
            context=context.as_text(),
        )

        sources = self._build_sources(
            retrieval.chunks
        )

        logger.info(
            "Question answered using %s retrieved chunks.",
            retrieval.count,
        )

        return QuestionResponse(
            question=question,
            answer=llm_response.answer,
            sources=sources,
            model=llm_response.model,
            retrieval_count=retrieval.count,
        )


qa_service = QAService(
    retrieval_service=__import__(
        "app.services.retrieval_service",
        fromlist=["retrieval_service"],
    ).retrieval_service,
    llm_service=llm_service,
)