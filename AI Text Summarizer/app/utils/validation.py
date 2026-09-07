from app.core.config import settings


def validate_input_length(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    if len(text) > settings.MAX_INPUT_CHARACTERS:
        raise ValueError(
            f"Text exceeds the maximum allowed length of "
            f"{settings.MAX_INPUT_CHARACTERS:,} characters."
        )


def validate_summary_lengths(
    min_length: int,
    max_length: int,
) -> None:
    if min_length < 10:
        raise ValueError(
            "Minimum summary length must be at least 10."
        )

    if max_length < min_length:
        raise ValueError(
            "Maximum summary length must be greater than "
            "or equal to minimum summary length."
        )

    if max_length > 2_000:
        raise ValueError(
            "Maximum summary length cannot exceed 2,000."
        )