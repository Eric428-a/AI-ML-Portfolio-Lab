# tests/test_schemas.py

import pytest
from pydantic import ValidationError

from app.schemas.question import QuestionRequest
from app.schemas.document import DocumentStatus
from app.schemas.response import SourceReference


def test_question_request_accepts_valid_question():
    request = QuestionRequest(
        question="What is this document about?"
    )

    assert request.question == "What is this document about?"


def test_question_request_rejects_empty_question():
    with pytest.raises(ValidationError):
        QuestionRequest(question="")


def test_question_request_accepts_top_k():
    request = QuestionRequest(
        question="What is the conclusion?",
        top_k=3,
    )

    assert request.top_k == 3


def test_document_status_contains_ready():
    assert DocumentStatus.READY.value == "ready"


def test_source_reference():
    source = SourceReference(
        document_id="doc-1",
        filename="report.pdf",
        page_number=2,
        relevance_score=0.91,
    )

    assert source.document_id == "doc-1"
    assert source.page_number == 2