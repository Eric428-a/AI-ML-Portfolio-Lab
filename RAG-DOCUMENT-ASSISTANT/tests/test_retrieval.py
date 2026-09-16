from app.rag.vector_store import VectorStore


class FakeEmbeddingModel:
    def embed(self, text):
        if "python" in text.lower():
            return [1.0, 0.0, 0.0]

        return [0.0, 1.0, 0.0]


def test_cosine_similarity():
    first = [1.0, 0.0, 0.0]
    second = [1.0, 0.0, 0.0]

    result = VectorStore._cosine_similarity(
        first,
        second,
    )

    assert result == 1.0


def test_cosine_similarity_different_vectors():
    first = [1.0, 0.0, 0.0]
    second = [0.0, 1.0, 0.0]

    result = VectorStore._cosine_similarity(
        first,
        second,
    )

    assert result == 0.0


def test_cosine_similarity_zero_vector():
    first = [0.0, 0.0, 0.0]
    second = [1.0, 0.0, 0.0]

    result = VectorStore._cosine_similarity(
        first,
        second,
    )

    assert result == 0.0