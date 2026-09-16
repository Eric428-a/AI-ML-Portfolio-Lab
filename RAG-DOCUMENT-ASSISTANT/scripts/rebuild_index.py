import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from app.db.database import SessionLocal
from app.db.models import DocumentChunk
from app.rag.vector_store import vector_store


def main() -> None:
    if vector_store.index_file.exists():
        vector_store.index_file.unlink()

    db = SessionLocal()

    try:
        chunks = (
            db.query(DocumentChunk)
            .order_by(
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
            )
            .all()
        )

        for chunk in chunks:
            vector_id = vector_store.add(
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                text=chunk.content,
            )

            chunk.vector_id = vector_id

        db.commit()

        print(
            f"Rebuilt vector index with {len(chunks)} chunks."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()