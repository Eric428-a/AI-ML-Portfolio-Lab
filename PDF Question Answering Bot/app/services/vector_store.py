from pathlib import Path

import chromadb

from app.core.config import settings
from app.core.logging import get_logger
from app.models.document import DocumentChunk
from app.models.chunk import RetrievedChunk

logger = get_logger(__name__)


class VectorStore:
    """Persistent Chroma vector store."""

    def __init__(
        self,
        persist_directory: str | None = None,
        collection_name: str | None = None,
    ) -> None:
        directory = Path(
            persist_directory
            or settings.CHROMA_PERSIST_DIRECTORY
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=(
                collection_name
                or settings.CHROMA_COLLECTION_NAME
            ),
            metadata={
                "hnsw:space": "cosine",
            },
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> int:
        if not chunks:
            return 0

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Each chunk must have exactly one embedding."
            )

        self.collection.upsert(
            ids=[chunk.id for chunk in chunks],
            embeddings=embeddings,
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "filename": chunk.filename,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                }
                for chunk in chunks
            ],
        )

        logger.info(
            "Stored %s chunks in vector database.",
            len(chunks),
        )

        return len(chunks)

    def query(
        self,
        embedding: list[float],
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[RetrievedChunk]:
        where = None

        if document_id:
            where = {
                "document_id": document_id,
            }

        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = (
            result.get("documents", [[]])[0]
            or []
        )

        metadatas = (
            result.get("metadatas", [[]])[0]
            or []
        )

        distances = (
            result.get("distances", [[]])[0]
            or []
        )

        ids = (
            result.get("ids", [[]])[0]
            or []
        )

        retrieved: list[RetrievedChunk] = []

        for index, chunk_id in enumerate(ids):
            metadata = metadatas[index]
            distance = float(distances[index])

            relevance_score = max(
                0.0,
                min(1.0, 1.0 - distance),
            )

            retrieved.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    document_id=str(
                        metadata.get("document_id", "")
                    ),
                    filename=str(
                        metadata.get("filename", "")
                    ),
                    page_number=int(
                        metadata.get("page_number", 1)
                    ),
                    text=str(
                        documents[index]
                        if index < len(documents)
                        else ""
                    ),
                    relevance_score=relevance_score,
                )
            )

        return retrieved

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        self.collection.delete(
            where={
                "document_id": document_id,
            }
        )

        logger.info(
            "Deleted vectors for document %s",
            document_id,
        )

    def count(self) -> int:
        return self.collection.count()


vector_store = VectorStore()