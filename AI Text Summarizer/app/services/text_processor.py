import re
from dataclasses import dataclass


@dataclass
class ProcessedText:
    original: str
    normalized: str
    sentences: list[str]
    words: list[str]


class TextProcessor:
    @staticmethod
    def normalize(text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def split_sentences(text: str) -> list[str]:
        normalized = TextProcessor.normalize(text)

        if not normalized:
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+(?=[A-Z0-9\"'])",
            normalized,
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    @staticmethod
    def extract_words(text: str) -> list[str]:
        return re.findall(
            r"\b[\w'-]+\b",
            text.lower(),
            flags=re.UNICODE,
        )

    @classmethod
    def process(cls, text: str) -> ProcessedText:
        normalized = cls.normalize(text)
        sentences = cls.split_sentences(normalized)
        words = cls.extract_words(normalized)

        return ProcessedText(
            original=text,
            normalized=normalized,
            sentences=sentences,
            words=words,
        )


text_processor = TextProcessor()