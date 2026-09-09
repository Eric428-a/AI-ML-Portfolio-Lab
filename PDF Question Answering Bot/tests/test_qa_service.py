from unittest.mock import MagicMock

from app.models.chunk import RetrievalResult, RetrievedChunk
from app.services.llm_service import LLMResponse, LLMService
from app.services.qa_service import QAService


def make_chunk() -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        filename="research.pdf",
        page_number=4,
        text="The project was completed in 2026.",
        relevance_score=0.91,
    )


def test_qa_service_returns_answer_and_sources() -> None:
    retrieval_service = MagicMock()
    llm_service = MagicMock()

    retrieval_service.retrieve.return_value = RetrievalResult(
        query="When was the project completed?",
        chunks=[make_chunk()],
    )

    llm_service.generate.return_value = LLMResponse(
        answer="The project was completed in 2026.",
        model="test-model",
    )

    service = QAService(
        retrieval_service=retrieval_service,
        llm_service=llm_service,
    )

    result = service.ask(
        question="When was the project completed?"
    )

    assert result.answer == (
        "The project was completed in 2026."
    )

    assert result.model == "test-model"
    assert result.retrieval_count == 1
    assert len(result.sources) == 1
    assert result.sources[0].page_number == 4


def test_qa_service_handles_no_relevant_chunks() -> None:
    retrieval_service = MagicMock()
    llm_service = MagicMock()

    retrieval_service.retrieve.return_value = RetrievalResult(
        query="Unknown question",
        chunks=[],
    )

    service = QAService(
        retrieval_service=retrieval_service,
        llm_service=llm_service,
    )

    result = service.ask(
        question="Unknown question"
    )

    assert result.retrieval_count == 0
    assert result.sources == []
    assert "could not find enough relevant" in (
        result.answer.lower()
    )

    llm_service.generate.assert_not_called()


def test_qa_context_contains_source_metadata() -> None:
    from app.services.qa_service import QAContext

    context = QAContext(
        chunks=[make_chunk()]
    )

    text = context.as_text()

    assert "research.pdf" in text
    assert "Page: 4" in text
    assert "completed in 2026" in text