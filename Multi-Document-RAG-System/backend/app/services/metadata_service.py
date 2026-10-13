from pathlib import Path
from typing import Any


def build_document_metadata(
    filename: str,
    content_type: str,
    file_size: int,
    checksum: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = Path(filename)

    metadata = {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "content_type": content_type,
        "file_size": file_size,
        "checksum": checksum,
    }

    if extra:
        metadata.update(extra)

    return metadata


def build_chunk_metadata(
    document_id: str,
    filename: str,
    chunk_index: int,
    chunk_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "document_id": document_id,
        "filename": filename,
        "chunk_index": chunk_index,
        **(chunk_metadata or {}),
    }