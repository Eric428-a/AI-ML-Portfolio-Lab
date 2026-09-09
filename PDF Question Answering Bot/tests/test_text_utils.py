# tests/test_text_utils.py

from app.utils.text_utils import (
    clean_text,
    count_words,
    split_sentences,
)


def test_clean_text_normalizes_whitespace():
    text = "  Hello   world.\n\nThis   is a test.  "

    result = clean_text(text)

    assert result == "Hello world. This is a test."


def test_clean_text_handles_empty_text():
    assert clean_text("") == ""
    assert clean_text(None) == ""


def test_count_words():
    assert count_words("Hello world from Python") == 4


def test_count_words_empty_text():
    assert count_words("") == 0


def test_split_sentences():
    text = "This is sentence one. This is sentence two! Is this sentence three?"

    result = split_sentences(text)

    assert len(result) == 3
    assert "sentence one" in result[0].lower()


def test_split_sentences_empty_text():
    assert split_sentences("") == []