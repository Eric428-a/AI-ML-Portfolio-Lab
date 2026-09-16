from dataclasses import dataclass

from app.db.database import SessionLocal
from app.db.models import DocumentChunk
from app.rag.vector_store import vector_store


@dataclass
class RetrievedChunk:
    document_id: int
    filename: str
    chunk_index: int
    page_number: int | None
    content: str
    score: float


class Retriever:
    def search(
        self,
        question: str,
        document_ids: list[int] | None,
        top_k: int,
    ) -> list[RetrievedChunk]:
        results = vector_store.search(
            query=question,
            top_k=top_k,
            document_ids=document_ids,
        )

        if not results:
            return []

        db = SessionLocal()

        try:
            retrieved = []

            for result in results:
                chunk = db.get(
                    DocumentChunk,
                    result["chunk_index"],
                )

                filename = "Unknown document"

                if chunk and chunk.document:
                    filename = chunk.document.filename

                retrieved.append(
                    RetrievedChunk(
                        document_id=result["document_id"],
                        filename=filename,
                        chunk_index=result["chunk_index"],
                        page_number=(
                            chunk.page_number
                            if chunk
                            else None
                        ),
                        content=result["text"],
                        score=result["score"],
                    )
                )

            return retrieved

        finally:
            db.close()


retriever = Retriever()