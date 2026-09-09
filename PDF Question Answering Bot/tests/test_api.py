# tests/test_api.py
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "PDF Question Answering Bot"
    assert "version" in data


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] in {"healthy", "degraded"}
    assert "service" in data


def test_api_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200


def test_documents_endpoint():
    response = client.get("/api/v1/documents")

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data


def test_questions_validation():
    response = client.post(
        "/api/v1/questions/ask",
        json={},
    )

    assert response.status_code == 422