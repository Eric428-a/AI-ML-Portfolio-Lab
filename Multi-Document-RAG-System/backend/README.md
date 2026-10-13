# Multi-Document RAG System — Backend

FastAPI backend for document ingestion, chunking, vector indexing,
retrieval, source citations, and conversational question answering.

## Requirements

- Python 3.11+
- pip
- A Groq API key or another supported LLM provider

## Installation

Create a virtual environment from this directory.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt


Configure .env and set LLM_API_KEY to your provider's API key.
Run
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


API documentation:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc
Run tests
pytest -q


Main endpoints
Method	Endpoint	Purpose
GET	/api/v1/health	Health check
GET	/api/v1/health/ready	Database readiness
POST	/api/v1/documents/upload	Upload documents
GET	/api/v1/documents	List documents
GET	/api/v1/documents/{id}	Retrieve document metadata
GET	/api/v1/documents/{id}/chunks	Inspect document chunks
PATCH	/api/v1/documents/{id}	Update metadata
DELETE	/api/v1/documents/{id}	Delete a document
POST	/api/v1/collections	Create a collection
GET	/api/v1/collections	List collections
GET	/api/v1/collections/{id}	Retrieve a collection
PATCH	/api/v1/collections/{id}	Update a collection
DELETE	/api/v1/collections/{id}	Delete a collection
POST	/api/v1/chat	Ask a document-grounded question
GET	/api/v1/chat/conversations	List conversations
GET	/api/v1/chat/conversations/{id}	Retrieve a conversation
PATCH	/api/v1/chat/conversations/{id}	Rename a conversation
DELETE	/api/v1/chat/conversations/{id}	Delete a conversation
Supported documents
- PDF
- DOCX
- TXT
- Markdown
- CSV
Scanned PDFs need OCR preprocessing before their text can be indexed.
Important
- Keep .env and API keys out of version control.
- Configure API authentication before exposing the API publicly.
- Use persistent storage for uploaded files and ChromaDB.
- The included SQLite database is suitable for local development.
- Production deployment should use database migrations and PostgreSQL.
- Do not expose the development server directly to the public internet.