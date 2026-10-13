from datetime import datetime, timezone

from app.schemas.chat_schema import ChatRequest, Citation, ChatResponse


def test_chat_request_defaults():
    request = ChatRequest(question="Summarize the documents.")

    assert request.question == "Summarize the documents."
    assert request.conversation_id is None
    assert request.include_sources is True


def test_chat_request_rejects_empty_question():
    from pydantic import ValidationError

    try:
        ChatRequest(question="")
    except ValidationError:
        return

    raise AssertionError("Empty questions must be rejected.")


def test_citation_schema():
    citation = Citation(
        document_id="doc-1",
        filename="report.pdf",
        chunk_id="chunk-1",
        chunk_index=0,
        text="Supporting evidence.",
        score=0.91,
        page=2,
    )

    assert citation.document_id == "doc-1"
    assert citation.page == 2


def test_chat_response_schema():
    response = ChatResponse(
        answer="The document describes the project.",
        conversation_id="conversation-1",
        message_id="message-1",
        citations=[],
        retrieved_chunks=0,
        model="test-model",
        created_at=datetime.now(timezone.utc),
    )

    assert response.answer
    assert response.citations == []