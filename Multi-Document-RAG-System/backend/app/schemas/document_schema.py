from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CollectionSummary(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class DocumentResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    status: str
    error_message: str | None = None
    chunk_count: int
    metadata_json: dict = Field(default_factory=dict)
    collection_id: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int
    page: int
    page_size: int


class DocumentUpdateRequest(BaseModel):
    filename: str | None = Field(default=None, min_length=1, max_length=255)
    collection_id: str | None = None
    metadata_json: dict | None = None


class DocumentUploadResponse(BaseModel):
    items: list[DocumentResponse]
    accepted: int
    failed: int


class DocumentChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    text: str
    metadata_json: dict = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)