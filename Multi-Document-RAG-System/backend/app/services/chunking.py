from dataclasses import dataclass


@dataclass
class TextChunk:
    text: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: dict


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    base_metadata: dict | None = None,
) -> list[TextChunk]:
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()

    if not text:
        return []

    chunks: list[TextChunk] = []
    start = 0
    index = 0
    step = chunk_size - chunk_overlap

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            boundary = max(
                text.rfind("\n", start, end),
                text.rfind(". ", start, end),
                text.rfind("? ", start, end),
                text.rfind("! ", start, end),
                text.rfind(" ", start, end),
            )

            if boundary > start + int(chunk_size * 0.55):
                end = boundary + 1

        content = text[start:end].strip()

        if content:
            chunks.append(
                TextChunk(
                    text=content,
                    chunk_index=index,
                    start_char=start,
                    end_char=end,
                    metadata={
                        **(base_metadata or {}),
                        "chunk_index": index,
                        "start_char": start,
                        "end_char": end,
                    },
                )
            )
            index += 1

        if end >= len(text):
            break

        start = max(start + 1, end - chunk_overlap)

    return chunks