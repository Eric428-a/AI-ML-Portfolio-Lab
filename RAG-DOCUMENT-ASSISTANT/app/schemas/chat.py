from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )

    document_ids: list[int] = Field(
        default_factory=list,
    )

    top_k: int | None = Field(
        default=None,
        ge=1,
        le=20,
    )


class SourceReference(BaseModel):
    document_id: int
    filename: str
    chunk_index: int
    page_number: int | None = None
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(
        default_factory=list,
    )