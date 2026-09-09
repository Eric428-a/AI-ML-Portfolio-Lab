from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=2000,
    )
    document_id: str | None = Field(
        default=None,
        max_length=100,
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = " ".join(value.split())

        if not value:
            raise ValueError("Question cannot be empty.")

        return value


class SourceReference(BaseModel):
    document_id: str
    filename: str
    page_number: int = Field(ge=1)
    chunk_id: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    excerpt: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceReference]
    model: str
    retrieval_count: int = Field(ge=0)