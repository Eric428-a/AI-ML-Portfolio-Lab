import pytest

from app.schemas.summarizer import SummaryStyle
from app.services.summarizer import (
    SummarizerService,
)


@pytest.fixture
def sample_text() -> str:
    return (
        "Artificial intelligence is changing "
        "many industries around the world. "
        "Machine learning systems can process "
        "large amounts of information and "
        "identify useful patterns. These systems "
        "are increasingly used in healthcare, "
        "finance, education, engineering, and "
        "business. Modern AI applications can "
        "also automate repetitive tasks and "
        "assist professionals with complex "
        "decision-making processes."
    )


@pytest.mark.asyncio
async def test_summarize(
    sample_text: str,
):
    service = SummarizerService()

    result = await service.summarize(
        text=sample_text,
        min_length=10,
        max_length=100,
        style=SummaryStyle.balanced,
    )

    assert result.summary
    assert result.original_word_count > 0
    assert result.summary_word_count > 0
    assert result.original_character_count > 0
    assert result.summary_character_count > 0
    assert 0 < result.compression_ratio <= 1


@pytest.mark.asyncio
async def test_concise_style(
    sample_text: str,
):
    service = SummarizerService()

    result = await service.summarize(
        text=sample_text,
        min_length=10,
        max_length=100,
        style=SummaryStyle.concise,
    )

    assert result.style == SummaryStyle.concise
    assert result.summary


@pytest.mark.asyncio
async def test_detailed_style(
    sample_text: str,
):
    service = SummarizerService()

    result = await service.summarize(
        text=sample_text,
        min_length=10,
        max_length=300,
        style=SummaryStyle.detailed,
    )

    assert result.style == SummaryStyle.detailed
    assert result.summary


@pytest.mark.asyncio
async def test_invalid_lengths(
    sample_text: str,
):
    service = SummarizerService()

    with pytest.raises(ValueError):
        await service.summarize(
            text=sample_text,
            min_length=100,
            max_length=20,
            style=SummaryStyle.balanced,
        )


@pytest.mark.asyncio
async def test_empty_text():
    service = SummarizerService()

    with pytest.raises(ValueError):
        await service.summarize(
            text="",
            min_length=10,
            max_length=100,
            style=SummaryStyle.balanced,
        )