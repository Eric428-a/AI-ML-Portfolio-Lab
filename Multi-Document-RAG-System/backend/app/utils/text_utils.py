import re
import unicodedata


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate_text(text: str, max_length: int = 1200) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."


def make_title(text: str, max_length: int = 60) -> str:
    normalized = normalize_text(text)
    first_line = normalized.split("\n", 1)[0].strip()

    if not first_line:
        return "New conversation"

    if len(first_line) > max_length:
        return first_line[: max_length - 3].rstrip() + "..."

    return first_line