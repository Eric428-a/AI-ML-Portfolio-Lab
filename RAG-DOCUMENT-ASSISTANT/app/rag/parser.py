from pathlib import Path


def parse_txt(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def parse_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages.append(text)

    return "\n\n".join(pages)


def parse_docx(path: Path) -> str:
    from docx import Document

    document = Document(str(path))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n\n".join(paragraphs)