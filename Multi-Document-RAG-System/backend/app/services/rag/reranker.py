import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


def _terms(text: str) -> list[str]:
    return re.findall(r"\b[a-zA-Z0-9_'-]+\b", text.lower())


def _lexical_score(query: str, text: str) -> float:
    query_terms = set(_terms(query))
    text_terms = _terms(text)

    if not query_terms or not text_terms:
        return 0.0

    counts = Counter(text_terms)
    matched = sum(1 for term in query_terms if counts[term] > 0)
    coverage = matched / len(query_terms)

    frequency = sum(
        min(counts[term], 3)
        for term in query_terms
    )

    frequency_score = min(
        frequency / max(len(query_terms) * 2, 1),
        1.0,
    )

    return 0.7 * coverage + 0.3 * frequency_score


def rerank_results(
    query: str,
    results: list[dict],
    limit: int | None = None,
) -> list[dict]:
    reranked = []

    for result in results:
        lexical = _lexical_score(
            query,
            str(result.get("text", "")),
        )
        semantic = float(result.get("score", 0.0))

        result_copy = dict(result)
        result_copy["semantic_score"] = semantic
        result_copy["lexical_score"] = lexical

        result_copy["rerank_score"] = (
            0.75 * semantic + 0.25 * lexical
        )

        reranked.append(result_copy)

    reranked.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    if limit is not None:
        return reranked[:limit]

    return reranked