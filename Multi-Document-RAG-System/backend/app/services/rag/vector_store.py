import logging
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import chromadb

from app.config import settings
from app.services.rag.embeddings import get_embedding_service

logger = logging.getLogger(__name__)


def _safe_collection_name(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_-]", "_", value)
    normalized = normalized.strip("_-")

    if not normalized:
        normalized = "default"

    if len(normalized) < 3:
        normalized = f"rag_{normalized}"

    return normalized[:63]


class VectorStore:
    def __init__(self):
        Path(settings.VECTOR_DB_DIR).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(settings.VECTOR_DB_DIR)
        )
        self.embeddings = get_embedding_service()

    def _collection(self, collection_id: str | None = None):
        identifier = _safe_collection_name(collection_id or "default")

        return self.client.get_or_create_collection(
            name=f"rag_{identifier}",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        document_id: str,
        filename: str,
        chunks: list[dict[str, Any]],
        collection_id: str | None = None,
    ) -> int:
        if not chunks:
            return 0

        texts = [str(chunk["text"]) for chunk in chunks]
        vectors = self.embeddings.embed_documents(texts)
        vector_collection = self._collection(collection_id)

        ids = [str(chunk["id"]) for chunk in chunks]

        metadatas = []

        for chunk in chunks:
            metadata = {
                "document_id": document_id,
                "filename": filename,
                "chunk_index": int(chunk["chunk_index"]),
            }

            for key, value in chunk.get("metadata_json", {}).items():
                if isinstance(value, (str, int, float, bool)):
                    metadata[key] = value

            metadatas.append(metadata)

        vector_collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=texts,
            metadatas=metadatas,
        )

        logger.info(
            "Indexed %d chunks for document %s",
            len(chunks),
            document_id,
        )

        return len(chunks)

    def search(
        self,
        query: str,
        top_k: int = 5,
        collection_id: str | None = None,
        document_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        vector_collection = self._collection(collection_id)

        if vector_collection.count() == 0:
            return []

        query_embedding = self.embeddings.embed_query(query)

        where = None

        if document_ids:
            if len(document_ids) == 1:
                where = {"document_id": document_ids[0]}
            else:
                where = {"document_id": {"$in": document_ids}}

        results = vector_collection.query(
            query_embeddings=[query_embedding],
            n_results=min(max(top_k, 1), vector_collection.count()),
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        matches = []

        for index, chunk_id in enumerate(ids):
            distance = float(distances[index]) if distances else 1.0
            score = max(0.0, min(1.0, 1.0 - distance))

            metadata = metadatas[index] if metadatas else {}

            matches.append(
                {
                    "chunk_id": chunk_id,
                    "text": documents[index] if documents else "",
                    "document_id": metadata.get("document_id", ""),
                    "filename": metadata.get("filename", "Unknown document"),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "score": score,
                    "metadata": metadata,
                }
            )

        return matches

    def delete_document(
        self,
        document_id: str,
        collection_id: str | None = None,
    ) -> None:
        vector_collection = self._collection(collection_id)

        vector_collection.delete(
            where={"document_id": document_id}
        )

        logger.info("Deleted vectors for document %s", document_id)

    def delete_collection(self, collection_id: str | None = None) -> None:
        name = f"rag_{_safe_collection_name(collection_id or 'default')}"

        try:
            self.client.delete_collection(name=name)
        except Exception:
            logger.debug("Vector collection %s did not exist", name)

    def count_chunks(self, collection_id: str | None = None) -> int:
        return self._collection(collection_id).count()


@lru_cache
def get_vector_store() -> VectorStore:
    return VectorStore()