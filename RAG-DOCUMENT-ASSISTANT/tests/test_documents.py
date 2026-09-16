from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_documents():
    response = client.get("/api/v1/documents")

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data
    assert "total" in data
    assert isinstance(data["documents"], list)


def test_upload_txt_document(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    monkeypatch.setattr(
        "app.services.document_service.settings.upload_dir",
        str(upload_dir),
    )

    content = b"This is a test document."

    response = client.post(
        "/api/v1/documents/upload",
        files={
            "file": (
                "test.txt",
                content,
                "text/plain",
            )
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["filename"] == "test.txt"
    assert data["file_type"] == "txt"
    assert data["status"] == "uploaded"