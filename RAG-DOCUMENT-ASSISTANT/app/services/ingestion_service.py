from pathlib import Path

from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import Document, DocumentChunk
from app.rag.chunker import chunk_text
from app.rag.loader import load_document
from app.rag.vector_store import vector_store


class IngestionService:
    def ingest(self, document_id: int) -> None:
        db = SessionLocal()

        try:
            document = db.get(Document, document_id)

            if document is None:
                raise ValueError(
                    f"Document {document_id} does not exist."
                )

            document.status = "processing"
            db.commit()

            text = load_document(
                Path(document.file_path)
            )

            chunks = chunk_text(
                text,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
            )

            for index, content in enumerate(chunks):
                vector_id = vector_store.add(
                    document_id=document.id,
                    chunk_index=index,
                    text=content,
                )

                db.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        content=content,
                        vector_id=vector_id,
                    )
                )

            document.chunk_count = len(chunks)
            document.status = "processed"

            db.commit()

        except Exception as exc:
            db.rollback()

            document = db.get(Document, document_id)

            if document:
                document.status = "failed"
                document.error_message = str(exc)
                db.commit()

            raise

        finally:
            db.close()


ingestion_service = IngestionService()