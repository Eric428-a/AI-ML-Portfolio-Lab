from dataclasses import dataclass


@dataclass(slots=True)
class RetrievedChunk:
    chunk_id: str
    document_id: str
    filename: str
    page_number: int
    text: str
    relevance_score: float


@dataclass(slots=True)
class EmbeddingResult:
    chunk_id: str
    vector: list[float]


@dataclass(slots=True)
class RetrievalResult:
    query: str
    chunks: list[RetrievedChunk]

    @property
    def count(self) -> int:
        return len(self.chunks)