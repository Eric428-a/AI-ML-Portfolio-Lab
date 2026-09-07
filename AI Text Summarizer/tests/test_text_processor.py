from app.services.text_processor import TextProcessor


def test_clean_text():
    processor = TextProcessor()

    result = processor.clean_text(
        "Hello    world.\n\n\nThis   is text."
    )

    assert result == "Hello world.\n\nThis is text."


def test_word_count():
    processor = TextProcessor()

    assert processor.word_count(
        "This is a simple test."
    ) == 5


def test_character_count():
    processor = TextProcessor()

    assert processor.character_count(
        "Hello"
    ) == 5


def test_sentence_count():
    processor = TextProcessor()

    assert processor.sentence_count(
        "First sentence. Second sentence!"
    ) == 2


def test_split_sentences():
    processor = TextProcessor()

    result = processor.split_into_sentences(
        "First sentence. Second sentence."
    )

    assert result == [
        "First sentence.",
        "Second sentence.",
    ]