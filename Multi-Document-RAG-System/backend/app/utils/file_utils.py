import hashlib
import re
from pathlib import Path
from uuid import uuid4


def calculate_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_filename(filename: str) -> str:
    name = Path(filename).name
    name = re.sub(r"[^A-Za-z0-9._ -]", "_", name)
    name = name.strip(" .")

    if not name:
        name = "document"

    return name[:200]


def make_storage_filename(original_filename: str) -> str:
    path = Path(safe_filename(original_filename))
    return f"{uuid4().hex}{path.suffix.lower()}"


def ensure_within_directory(path: Path, directory: Path) -> Path:
    resolved_path = path.resolve()
    resolved_directory = directory.resolve()

    if resolved_path != resolved_directory and resolved_directory not in resolved_path.parents:
        raise ValueError("Path escapes the permitted storage directory.")

    return resolved_path