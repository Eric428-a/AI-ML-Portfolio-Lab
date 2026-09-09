# scripts/evaluate.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from time import perf_counter

from app.services.qa_service import qa_service


def load_questions(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Evaluation file must contain a JSON array.")

    return data


def evaluate(questions: list[dict]) -> dict:
    results = []
    latencies = []

    for item in questions:
        question = str(item.get("question", "")).strip()
        document_id = item.get("document_id")
        expected_keywords = [
            str(keyword).lower()
            for keyword in item.get("expected_keywords", [])
        ]

        if not question:
            continue

        started = perf_counter()

        try:
            response = qa_service.ask(
                question=question,
                document_id=document_id,
                top_k=item.get("top_k"),
            )

            latency = perf_counter() - started
            latencies.append(latency)

            answer = response.answer.lower()

            keyword_hits = sum(
                1
                for keyword in expected_keywords
                if keyword in answer
            )

            keyword_score = (
                keyword_hits / len(expected_keywords)
                if expected_keywords
                else None
            )

            results.append(
                {
                    "question": question,
                    "answer": response.answer,
                    "sources": len(response.sources),
                    "latency_seconds": round(latency, 4),
                    "keyword_score": keyword_score,
                }
            )

        except Exception as exc:
            results.append(
                {
                    "question": question,
                    "error": str(exc),
                }
            )

    valid_scores = [
        item["keyword_score"]
        for item in results
        if item.get("keyword_score") is not None
    ]

    valid_latencies = [
        item["latency_seconds"]
        for item in results
        if "latency_seconds" in item
    ]

    return {
        "total_questions": len(results),
        "successful_questions": sum(
            1 for item in results if "error" not in item
        ),
        "failed_questions": sum(
            1 for item in results if "error" in item
        ),
        "average_keyword_score": (
            round(mean(valid_scores), 4)
            if valid_scores
            else None
        ),
        "average_latency_seconds": (
            round(mean(valid_latencies), 4)
            if valid_latencies
            else None
        ),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate the PDF question answering system."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to evaluation JSON file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evaluation-results.json"),
        help="Output JSON path.",
    )

    args = parser.parse_args()

    questions = load_questions(args.input)
    report = evaluate(questions)

    with args.output.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()