from pathlib import Path

from app.rag.parser import parse_docx, parse_pdf, parse_txt


def load_document(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {path}"
        )

    extension = path.suffix.lower()

    if extension == ".pdf":
        return parse_pdf(path)

    if extension == ".docx":
        return parse_docx(path)

    if extension == ".txt":
        return parse_txt(path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )