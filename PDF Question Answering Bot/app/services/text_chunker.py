from dataclasses import dataclass

from app.core.logging import get_logger
from app.models.document import DocumentChunk, DocumentPage
from app.utils.validation import validate_chunk_parameters

logger = get_logger(__name__)


@dataclass(slots=True)
class ChunkingResult:
    document_id: str
    chunks: list[DocumentChunk]
    chunk_count: int


class TextChunker:
    """Split document pages into overlapping retrieval chunks."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> None:
        validate_chunk_parameters(
            chunk_size,
            chunk_overlap,
        )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _split_words(
        self,
        text: str,
    ) -> list[str]:
        return text.split()

    def _create_windows(
        self,
        words: list[str],
    ) -> list[list[str]]:
        if not words:
            return []

        windows: list[list[str]] = []

        step = self.chunk_size - self.chunk_overlap
        start = 0

        while start < len(words):
            end = min(
                start + self.chunk_size,
                len(words),
            )

            window = words[start:end]

            if window:
                windows.append(window)

            if end >= len(words):
                break

            start += step

        return windows

    def chunk_page(
        self,
        page: DocumentPage,
        filename: str,
        starting_index: int = 0,
    ) -> list[DocumentChunk]:
        words = self._split_words(page.text)

        windows = self._create_windows(words)
        chunks: list[DocumentChunk] = []

        for offset, window in enumerate(windows):
            chunk_index = starting_index + offset

            chunk_id = (
                f"{page.document_id}"
                f"-page-{page.page_number}"
                f"-chunk-{chunk_index}"
            )

            text = " ".join(window)

            chunks.append(
                DocumentChunk(
                    id=chunk_id,
                    document_id=page.document_id,
                    filename=filename,
                    page_number=page.page_number,
                    text=text,
                    chunk_index=chunk_index,
                    metadata={
                        "document_id": page.document_id,
                        "filename": filename,
                        "page_number": page.page_number,
                        "chunk_index": chunk_index,
                    },
                )
            )

        return chunks

    def chunk_pages(
        self,
        pages: list[DocumentPage],
        filename: str,
    ) -> ChunkingResult:
        if not pages:
            return ChunkingResult(
                document_id="",
                chunks=[],
                chunk_count=0,
            )

        document_id = pages[0].document_id

        all_chunks: list[DocumentChunk] = []
        next_index = 0

        for page in pages:
            page_chunks = self.chunk_page(
                page=page,
                filename=filename,
                starting_index=next_index,
            )

            all_chunks.extend(page_chunks)
            next_index += len(page_chunks)

        logger.info(
            "Document %s chunked into %s chunks",
            document_id,
            len(all_chunks),
        )

        return ChunkingResult(
            document_id=document_id,
            chunks=all_chunks,
            chunk_count=len(all_chunks),
        )


text_chunker = TextChunker()