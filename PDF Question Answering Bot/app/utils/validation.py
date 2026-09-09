from pathlib import Path


def validate_file_extension(
    filename: str,
    allowed_extensions: list[str],
) -> bool:
    extension = Path(filename).suffix.lower()

    return extension in {
        item.lower()
        if item.startswith(".")
        else f".{item.lower()}"
        for item in allowed_extensions
    }


def validate_file_size(
    size_bytes: int,
    maximum_megabytes: int,
) -> bool:
    maximum_bytes = maximum_megabytes * 1024 * 1024

    return 0 < size_bytes <= maximum_bytes


def validate_chunk_parameters(
    chunk_size: int,
    chunk_overlap: int,
) -> None:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )


def validate_top_k(top_k: int) -> None:
    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20.")