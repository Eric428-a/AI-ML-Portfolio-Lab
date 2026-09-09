# README.md

# PDF Question Answering Bot

A production-oriented Retrieval-Augmented Generation system that allows users to upload PDF documents and ask questions about their contents.

## Features

- PDF upload
- PDF text extraction
- Page-aware processing
- Intelligent text chunking
- Semantic embeddings
- ChromaDB vector search
- Retrieval-Augmented Generation
- Groq LLM integration
- Source attribution
- Document management
- Vanilla JavaScript frontend
- FastAPI backend
- Docker support
- Render deployment configuration
- Automated tests
- Ruff and Black linting
- Dependency security auditing

## Architecture

```text
PDF
 │
 ▼
Extraction
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Semantic Retrieval
 │
 ▼
Groq LLM
 │
 ▼
Answer + Sources

Technology Stack
Backend
Python
FastAPI
Pydantic
Uvicorn
AI / RAG
Sentence Transformers
ChromaDB
Groq
PDF
pypdf
Frontend
HTML
CSS
Vanilla JavaScript
Deployment
Docker
Docker Compose
Render
GitHub Actions
Project Structure
pdf-question-answering-bot/
├── app/
├── frontend/
├── data/
├── models/
├── tests/
├── scripts/
├── docs/
├── .github/
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── pyproject.toml
└── README.md
Quick Start

Create the environment:

python -m venv .venv

Windows:

.venv\Scripts\Activate.ps1

Install:

pip install -r requirements.txt

Create .env from .env.example.

Configure:

GROQ_API_KEY=your_groq_api_key

Run:

uvicorn app.main:app --reload

Open:

http://localhost:8000
API

API prefix:

/api/v1

Documentation:

/docs

Main endpoints:

GET    /api/v1/health
POST   /api/v1/documents/upload
GET    /api/v1/documents
GET    /api/v1/documents/{document_id}
DELETE /api/v1/documents/{document_id}
POST   /api/v1/questions/ask
Docker
docker compose up --build
Testing
pytest
Linting
ruff check app tests scripts
black --check app tests scripts
Security
pip-audit
RAG Configuration

Default configuration:

Chunk size: 1000
Chunk overlap: 150
Top-K retrieval: 5
Minimum relevance score: 0.25
Embedding model: all-MiniLM-L6-v2
LLM: llama-3.3-70b-versatile
Vector store: ChromaDB
Environment Variables

See:

.env.example

for the complete configuration.

Documentation

Detailed documentation is available in:

docs/
├── architecture.md
├── api.md
├── rag_pipeline.md
├── usage.md
└── deployment.md
License

This project is distributed under the license included in LICENSE.