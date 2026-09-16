import json
import math
from pathlib import Path

from app.core.config import settings
from app.core.security import generate_id
from app.rag.embeddings import embedding_model


class VectorStore:
    def __init__(self) -> None:
        self.path = Path(
            settings.vector_store_path
        )
        self.path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.index_file = self.path / "index.json"

    def _load(self) -> list[dict]:
        if not self.index_file.exists():
            return []

        try:
            return json.loads(
                self.index_file.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError:
            return []

    def _save(self, records: list[dict]) -> None:
        self.index_file.write_text(
            json.dumps(
                records,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def add(
        self,
        document_id: int,
        chunk_index: int,
        text: str,
    ) -> str:
        records = self._load()

        vector_id = generate_id()
        embedding = embedding_model.embed(text)

        records.append(
            {
                "id": vector_id,
                "document_id": document_id,
                "chunk_index": chunk_index,
                "text": text,
                "embedding": embedding,
            }
        )

        self._save(records)

        return vector_id

    def search(
        self,
        query: str,
        top_k: int,
        document_ids: list[int] | None = None,
    ) -> list[dict]:
        records = self._load()

        if document_ids:
            records = [
                record
                for record in records
                if record["document_id"] in document_ids
            ]

        if not records:
            return []

        query_vector = embedding_model.embed(query)

        scored = []

        for record in records:
            score = self._cosine_similarity(
                query_vector,
                record["embedding"],
            )

            scored.append(
                (
                    score,
                    record,
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            {
                **record,
                "score": score,
            }
            for score, record in scored[:top_k]
        ]

    @staticmethod
    def _cosine_similarity(
        first: list[float],
        second: list[float],
    ) -> float:
        if not first or not second:
            return 0.0

        dot = sum(
            a * b
            for a, b in zip(first, second)
        )

        first_norm = math.sqrt(
            sum(value * value for value in first)
        )

        second_norm = math.sqrt(
            sum(value * value for value in second)
        )

        if first_norm == 0 or second_norm == 0:
            return 0.0

        return dot / (
            first_norm * second_norm
        )


vector_store = VectorStore()