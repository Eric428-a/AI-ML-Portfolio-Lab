def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[str]:
    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    words = text.split()

    chunks = []
    start = 0

    words_per_overlap = max(
        1,
        int(
            chunk_size
            * chunk_overlap
            / chunk_size
        ),
    )

    while start < len(words):
        current_words = []
        current_length = 0
        index = start

        while index < len(words):
            word = words[index]

            additional_length = len(word)

            if current_words:
                additional_length += 1

            if (
                current_length + additional_length
                > chunk_size
            ):
                break

            current_words.append(word)
            current_length += additional_length
            index += 1

        if not current_words:
            current_words.append(words[index])
            index += 1

        chunks.append(" ".join(current_words))

        if index >= len(words):
            break

        next_start = index - words_per_overlap

        if next_start <= start:
            next_start = start + 1

        start = next_start

    return chunks