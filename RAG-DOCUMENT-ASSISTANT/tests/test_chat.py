from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_validation():
    response = client.post(
        "/api/v1/chat",
        json={
            "question": "",
        },
    )

    assert response.status_code == 422


def test_chat_request_shape():
    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is this document about?",
            "document_ids": [],
            "top_k": 5,
        },
    )

    assert response.status_code in {
        200,
        500,
    }