from abc import ABC, abstractmethod
from collections import Counter

from app.services.text_processor import text_processor
from app.utils.text import count_words


class BaseModelService(ABC):
    @abstractmethod
    def summarize(
        self,
        text: str,
        min_length: int,
        max_length: int,
        style: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> dict:
        raise NotImplementedError


class ExtractiveModelService(BaseModelService):
    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be",
        "by", "for", "from", "has", "he", "in", "is",
        "it", "its", "of", "on", "that", "the", "to",
        "was", "were", "will", "with", "this", "these",
        "those", "or", "but", "if", "then", "than",
        "they", "their", "them", "we", "our", "you",
        "your", "i", "me", "my", "not", "can", "could",
        "would", "should", "have", "had", "do", "does",
        "did", "about", "into", "over", "after", "before",
    }

    def _score_words(self, words: list[str]) -> Counter:
        filtered = [
            word
            for word in words
            if word not in self.STOP_WORDS
            and len(word) > 2
        ]

        frequencies = Counter(filtered)

        if not frequencies:
            return Counter()

        maximum = max(frequencies.values())

        for word in frequencies:
            frequencies[word] /= maximum

        return frequencies

    def _score_sentence(
        self,
        sentence: str,
        frequencies: Counter,
    ) -> float:
        words = text_processor.extract_words(sentence)

        if not words:
            return 0.0

        score = sum(
            frequencies.get(word, 0)
            for word in words
        )

        return score / len(words)

    def summarize(
        self,
        text: str,
        min_length: int,
        max_length: int,
        style: str,
    ) -> str:
        processed = text_processor.process(text)
        sentences = processed.sentences

        if not sentences:
            return text.strip()

        if len(sentences) == 1:
            return sentences[0]

        frequencies = self._score_words(processed.words)

        scored = [
            (
                index,
                sentence,
                self._score_sentence(
                    sentence,
                    frequencies,
                ),
            )
            for index, sentence in enumerate(sentences)
        ]

        scored.sort(
            key=lambda item: item[2],
            reverse=True,
        )

        original_words = count_words(text)

        if style == "concise":
            target_ratio = 0.20
        elif style == "detailed":
            target_ratio = 0.45
        else:
            target_ratio = 0.30

        target_words = max(
            min_length,
            int(original_words * target_ratio),
        )

        target_words = min(
            target_words,
            max_length,
        )

        selected = []
        current_words = 0

        for index, sentence, _score in scored:
            sentence_words = count_words(sentence)

            if (
                selected
                and current_words + sentence_words > max_length
            ):
                continue

            selected.append((index, sentence))
            current_words += sentence_words

            if current_words >= target_words:
                break

        if not selected:
            selected = [(scored[0][0], scored[0][1])]

        selected.sort(key=lambda item: item[0])

        result = " ".join(
            sentence
            for _, sentence in selected
        ).strip()

        if len(result) > max_length:
            words = result.split()
            result = " ".join(words[:max_length]).strip()

        return result

    def health(self) -> dict:
        return {
            "status": "healthy",
            "provider": "local",
            "model": "extractive-summarizer-v1",
        }


class ModelServiceFactory:
    @staticmethod
    def create() -> BaseModelService:
        return ExtractiveModelService()


model_service = ModelServiceFactory.create()