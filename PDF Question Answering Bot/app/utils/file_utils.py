import hashlib
import re
from pathlib import Path
from uuid import uuid4


def generate_document_id() -> str:
    return uuid4().hex


def calculate_file_hash(file_path: str | Path) -> str:
    path = Path(file_path)

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def sanitize_filename(filename: str) -> str:
    filename = Path(filename).name

    filename = re.sub(
        r"[^A-Za-z0-9._ -]",
        "_",
        filename,
    )

    filename = re.sub(
        r"\s+",
        " ",
        filename,
    ).strip()

    return filename or "document.pdf"


def is_pdf_filename(filename: str) -> bool:
    return Path(filename).suffix.lower() == ".pdf"


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory