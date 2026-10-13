from app.services.chunking import split_text
from app.services.rag.prompts import SYSTEM_PROMPT, build_rag_prompt
from app.services.rag.reranker import rerank_results


def test_prompt_contains_question_and_document_evidence():
    prompt = build_rag_prompt(
        "What is the project name?",
        [
            {
                "chunk_id": "chunk-1",
                "filename": "project.txt",
                "chunk_index": 0,
                "text": "The project is called Multi-Document RAG System.",
            }
        ],
    )

    assert "What is the project name?" in prompt
    assert "Multi-Document RAG System" in prompt
    assert "chunk-1" in prompt


def test_empty_context_prompt():
    prompt = build_rag_prompt("What is the answer?", [])

    assert "No relevant document excerpts" in prompt
    assert "What is the answer?" in prompt


def test_system_prompt_contains_grounding_rules():
    assert "Never invent facts" in SYSTEM_PROMPT
    assert "untrusted evidence" in SYSTEM_PROMPT


def test_reranker_returns_most_relevant_first():
    results = [
        {
            "chunk_id": "irrelevant",
            "text": "Weather information about a distant location.",
            "score": 0.4,
        },
        {
            "chunk_id": "relevant",
            "text": "FastAPI is used to build a Python API.",
            "score": 0.8,
        },
    ]

    ranked = rerank_results("FastAPI Python API", results)

    assert ranked[0]["chunk_id"] == "relevant"
    assert "rerank_score" in ranked[0]


def test_reranker_respects_limit():
    results = [
        {"text": "alpha", "score": 0.8},
        {"text": "beta", "score": 0.7},
        {"text": "gamma", "score": 0.6},
    ]

    assert len(rerank_results("alpha", results, limit=2)) == 2


def test_chunk_metadata_preserved():
    chunks = split_text(
        "Sample document content " * 20,
        chunk_size=100,
        chunk_overlap=10,
        base_metadata={"document_id": "doc-1"},
    )

    assert chunks
    assert chunks[0].metadata["document_id"] == "doc-1"