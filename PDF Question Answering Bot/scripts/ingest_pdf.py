import argparse
from pathlib import Path

from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.services.embedding_service import embedding_service
from app.services.pdf_service import pdf_service
from app.services.text_chunker import text_chunker
from app.services.text_extractor import text_extractor
from app.services.vector_store import vector_store
from app.utils.file_utils import (
    calculate_file_hash,
    generate_document_id,
    sanitize_filename,
)

logger = get_logger(__name__)


def ingest(pdf_path: Path) -> dict[str, object]:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    filename = sanitize_filename(
        pdf_path.name
    )

    document_id = generate_document_id()

    logger.info(
        "Starting ingestion: %s",
        filename,
    )

    extraction = text_extractor.extract(
        file_path=str(pdf_path),
        document_id=document_id,
    )

    chunking = text_chunker.chunk_pages(
        pages=extraction.pages,
        filename=filename,
    )

    if not chunking.chunks:
        raise ValueError(
            "No extractable text was found in the PDF."
        )

    embeddings = embedding_service.embed_chunks(
        chunking.chunks
    )

    vectors = [
        item.vector
        for item in embeddings
    ]

    stored_count = vector_store.add_chunks(
        chunks=chunking.chunks,
        embeddings=vectors,
    )

    result = {
        "document_id": document_id,
        "filename": filename,
        "file_hash": calculate_file_hash(pdf_path),
        "pages": extraction.page_count,
        "words": extraction.total_words,
        "chunks": chunking.chunk_count,
        "stored_vectors": stored_count,
    }

    logger.info(
        "Ingestion complete: %s",
        result,
    )

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest a PDF into the RAG vector store."
    )

    parser.add_argument(
        "pdf",
        type=Path,
        help="Path to the PDF file.",
    )

    args = parser.parse_args()

    configure_logging()

    result = ingest(args.pdf)

    print("\nIngestion complete:")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()