from datetime import datetime

from pydantic import BaseModel, Field


class Citation(BaseModel):
    document_id: str
    filename: str
    chunk_id: str
    chunk_index: int
    text: str
    score: float | None = None
    page: int | None = None


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None
    collection_id: str | None = None
    document_ids: list[str] | None = None
    top_k: int | None = Field(default=None, ge=1, le=30)
    include_sources: bool = True


class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
    message_id: str
    citations: list[Citation] = Field(default_factory=list)
    retrieved_chunks: int = 0
    model: str
    created_at: datetime


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    citations: list[dict] = Field(default_factory=list)
    created_at: datetime


class ConversationResponse(BaseModel):
    id: str
    title: str
    collection_id: str | None = None
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse] = Field(default_factory=list)


class ConversationListResponse(BaseModel):
    items: list[ConversationResponse]
    total: int


class RenameConversationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)