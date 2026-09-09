import argparse
from pathlib import Path

from app.core.config import settings
from app.core.logging import configure_logging
from app.services.document_service import document_service
from app.services.embedding_service import embedding_service
from app.services.text_chunker import text_chunker
from app.services.text_extractor import text_extractor
from app.services.vector_store import vector_store


def rebuild_from_directory(
    directory: Path,
) -> int:
    if not directory.exists():
        raise FileNotFoundError(
            f"Directory not found: {directory}"
        )

    pdf_files = sorted(
        directory.glob("*.pdf")
    )

    if not pdf_files:
        print("No PDF files found.")
        return 0

    processed = 0

    for pdf_file in pdf_files:
        print(
            f"\nProcessing: {pdf_file.name}"
        )

        document = document_service.create_document(
            filename=pdf_file.name,
            content_type="application/pdf",
            size_bytes=pdf_file.stat().st_size,
        )

        try:
            extraction = text_extractor.extract(
                file_path=str(pdf_file),
                document_id=document.id,
            )

            chunking = text_chunker.chunk_pages(
                pages=extraction.pages,
                filename=document.filename,
            )

            if not chunking.chunks:
                print(
                    "Skipped: no extractable text."
                )
                continue

            embeddings = embedding_service.embed_chunks(
                chunking.chunks
            )

            vector_store.add_chunks(
                chunks=chunking.chunks,
                embeddings=[
                    item.vector
                    for item in embeddings
                ],
            )

            document.page_count = (
                extraction.page_count
            )
            document.chunk_count = (
                chunking.chunk_count
            )
            document.status = "ready"

            processed += 1

            print(
                f"Ready: {document.page_count} pages, "
                f"{document.chunk_count} chunks"
            )

        except Exception as exc:
            document.status = "failed"

            print(
                f"Failed: {exc}"
            )

    return processed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild the PDF vector index."
    )

    parser.add_argument(
        "--directory",
        type=Path,
        default=Path(settings.UPLOAD_DIRECTORY),
        help="Directory containing PDF files.",
    )

    args = parser.parse_args()

    configure_logging()

    processed = rebuild_from_directory(
        args.directory
    )

    print(
        f"\nProcessed {processed} PDF file(s)."
    )


if __name__ == "__main__":
    main()