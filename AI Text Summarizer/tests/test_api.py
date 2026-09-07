from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


SAMPLE_TEXT = (
    "Artificial intelligence is changing "
    "many industries around the world. "
    "Machine learning systems can process "
    "large amounts of information and "
    "identify useful patterns. These systems "
    "are increasingly used in healthcare, "
    "finance, education, engineering, and "
    "business. Modern AI applications can "
    "also automate repetitive tasks."
)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == (
        "AI Text Summarizer"
    )

    assert data["status"] == "online"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == (
        "healthy"
    )


def test_summarizer_health():
    response = client.get(
        "/api/v1/summarizer/health"
    )

    assert response.status_code == 200

    assert response.json()["service"] == (
        "summarizer"
    )


def test_summarize():
    response = client.post(
        "/api/v1/summarizer/summarize",
        json={
            "text": SAMPLE_TEXT,
            "min_length": 10,
            "max_length": 100,
            "style": "balanced",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]
    assert data["original_word_count"] > 0
    assert data["summary_word_count"] > 0
    assert "compression_ratio" in data
    assert data["style"] == "balanced"


def test_empty_text_rejected():
    response = client.post(
        "/api/v1/summarizer/summarize",
        json={
            "text": "",
            "min_length": 10,
            "max_length": 100,
            "style": "balanced",
        },
    )

    assert response.status_code == 422


def test_invalid_style_rejected():
    response = client.post(
        "/api/v1/summarizer/summarize",
        json={
            "text": SAMPLE_TEXT,
            "min_length": 10,
            "max_length": 100,
            "style": "invalid",
        },
    )

    assert response.status_code == 422