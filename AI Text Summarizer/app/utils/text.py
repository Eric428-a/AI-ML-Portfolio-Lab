import re


def count_words(text: str) -> int:
    return len(
        re.findall(
            r"\b[\w'-]+\b",
            text,
            flags=re.UNICODE,
        )
    )


def count_characters(text: str) -> int:
    return len(text)


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def truncate_text(
    text: str,
    max_characters: int,
) -> str:
    if len(text) <= max_characters:
        return text

    return text[:max_characters].rsplit(" ", 1)[0] + "..."


def compression_ratio(
    original: str,
    summary: str,
) -> float:
    original_count = count_words(original)
    summary_count = count_words(summary)

    if original_count == 0:
        return 0.0

    return round(
        summary_count / original_count,
        4,
    )