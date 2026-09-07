from enum import Enum

from pydantic import BaseModel, Field, field_validator


class SummaryStyle(str, Enum):
    CONCISE = "concise"
    BALANCED = "balanced"
    DETAILED = "detailed"


class SummaryRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=50,
        max_length=100_000,
        description="Text to summarize.",
    )

    min_length: int = Field(
        default=30,
        ge=10,
        le=1_000,
    )

    max_length: int = Field(
        default=150,
        ge=20,
        le=2_000,
    )

    style: SummaryStyle = Field(
        default=SummaryStyle.BALANCED,
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Text cannot be empty.")

        return value

    @field_validator("max_length")
    @classmethod
    def validate_max_length(
        cls,
        value: int,
        info,
    ) -> int:
        min_length = info.data.get("min_length")

        if min_length is not None and value < min_length:
            raise ValueError(
                "max_length must be greater than or equal to min_length."
            )

        return value


class SummaryResponse(BaseModel):
    summary: str
    original_character_count: int
    summary_character_count: int
    original_word_count: int
    summary_word_count: int
    compression_ratio: float
    style: SummaryStyle
    model: str