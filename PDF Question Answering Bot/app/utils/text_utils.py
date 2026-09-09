import re


def normalize_whitespace(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = [
        re.sub(r"[ \t]+", " ", line).strip()
        for line in text.split("\n")
    ]

    return "\n".join(
        line
        for line in lines
        if line
    ).strip()


def clean_text(text: str) -> str:
    text = normalize_whitespace(text)

    text = re.sub(
        r"(?<!\n)\n(?!\n)",
        " ",
        text,
    )

    text = re.sub(
        r"[ ]{2,}",
        " ",
        text,
    )

    return text.strip()


def count_words(text: str) -> int:
    return len(
        re.findall(
            r"\b[\w'-]+\b",
            text,
            flags=re.UNICODE,
        )
    )


def split_sentences(text: str) -> list[str]:
    cleaned = clean_text(text)

    if not cleaned:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])",
        cleaned,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]