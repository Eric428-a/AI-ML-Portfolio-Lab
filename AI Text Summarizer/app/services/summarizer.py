from app.core.config import settings
from app.schemas.summarizer import SummaryResponse, SummaryStyle
from app.services.model_service import model_service
from app.utils.text import (
    compression_ratio,
    count_characters,
    count_words,
)
from app.utils.validation import (
    validate_input_length,
    validate_summary_lengths,
)


class SummarizerService:
    async def summarize(
        self,
        text: str,
        min_length: int,
        max_length: int,
        style: SummaryStyle,
    ) -> SummaryResponse:
        validate_input_length(text)

        validate_summary_lengths(
            min_length,
            max_length,
        )

        summary = model_service.summarize(
            text=text,
            min_length=min_length,
            max_length=max_length,
            style=style.value,
        )

        return SummaryResponse(
            summary=summary,
            original_character_count=count_characters(text),
            summary_character_count=count_characters(summary),
            original_word_count=count_words(text),
            summary_word_count=count_words(summary),
            compression_ratio=compression_ratio(
                text,
                summary,
            ),
            style=style,
            model=settings.MODEL_NAME,
        )

    async def health(self) -> dict:
        return model_service.health()


summarizer_service = SummarizerService()