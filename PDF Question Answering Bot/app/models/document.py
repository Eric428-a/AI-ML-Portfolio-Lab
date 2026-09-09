from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class Document:
    id: str
    filename: str
    content_type: str
    size_bytes: int
    page_count: int = 0
    chunk_count: int = 0
    status: str = "uploaded"
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(slots=True)
class DocumentPage:
    document_id: str
    page_number: int
    text: str


@dataclass(slots=True)
class DocumentChunk:
    id: str
    document_id: str
    filename: str
    page_number: int
    text: str
    chunk_index: int
    metadata: dict[str, str | int | float] = field(default_factory=dict)