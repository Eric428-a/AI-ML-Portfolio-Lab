# docs/architecture.md

# Architecture

## Overview

The PDF Question Answering Bot is a Retrieval-Augmented Generation (RAG) application.

The system accepts PDF documents, extracts their text, splits the text into chunks, generates vector embeddings, stores those vectors in ChromaDB, retrieves relevant chunks for user questions, and sends the retrieved context to an LLM.

## Architecture Flow

```text
User
 │
 ▼
Vanilla JavaScript Frontend
 │
 ▼
FastAPI API
 │
 ├── Document Routes
 │      │
 │      ▼
 │   Document Service
 │      │
 │      ├── PDF Service
 │      ├── Text Extractor
 │      ├── Text Chunker
 │      ├── Embedding Service
 │      └── Vector Store
 │
 └── Question Routes
        │
        ▼
     QA Service
        │
        ├── Retrieval Service
        │      │
        │      ├── Embedding Service
        │      └── Vector Store
        │
        └── LLM Service
               │
               ▼
             Groq


Main Components
FastAPI

FastAPI provides the HTTP API and application lifecycle management.

PDF Processing

PDFService reads PDF files using pypdf.

Text Extraction

TextExtractor converts PDF pages into structured text.

Chunking

TextChunker splits extracted text into overlapping chunks.

Embeddings

EmbeddingService uses Sentence Transformers to convert text into numerical vectors.

Vector Database

ChromaDB provides persistent vector storage and similarity search.

Retrieval

RetrievalService embeds the user's question and retrieves semantically relevant document chunks.

LLM

LLMService sends retrieved context and the user's question to Groq.

QA Orchestration

QAService coordinates retrieval, context construction, LLM generation, and source attribution.

Data Flow
User uploads a PDF.
API validates the file.
PDF is stored locally.
Pages are extracted.
Text is cleaned.
Text is divided into chunks.
Chunks are embedded.
Embeddings are stored in ChromaDB.
User submits a question.
Question is embedded.
Similar chunks are retrieved.
Relevant context is constructed.
Context is sent to the LLM.
Generated answer is returned with source references.
Storage
data/
├── uploads/
│   └── original PDF files
├── processed/
│   └── extracted text
└── chroma/
    └── persistent vector database
Security

The application includes:

File extension validation
File size validation
Filename sanitization
HTTP security headers
CORS configuration
Environment-based secrets
Dependency security auditing
Scalability

For production deployments, the local components can be replaced with managed infrastructure:

Object storage instead of local uploads
PostgreSQL or another metadata database
Managed vector database
Background workers for ingestion
Redis for queues and caching
Cloud-hosted LLM services

```markdown
# docs/api.md

# API Documentation

Base URL:

```text
/api/v1
Health
GET /health

Returns application health information.

Example:

GET /api/v1/health
Upload Document
POST /documents/upload

Uploads and processes a PDF document.

Request:

Content-Type: multipart/form-data

Form field:

file

Example response:

{
  "id": "document-id",
  "filename": "example.pdf",
  "content_type": "application/pdf",
  "size_bytes": 102400,
  "page_count": 10,
  "chunk_count": 25,
  "status": "ready"
}
List Documents
GET /documents

Returns all registered documents.

Example:

GET /api/v1/documents
Get Document
GET /documents/{document_id}

Returns a single document.

Example:

GET /api/v1/documents/document-id
Delete Document
DELETE /documents/{document_id}

Deletes a document and its associated vector data.

Example:

DELETE /api/v1/documents/document-id
Ask Question
POST /questions/ask

Ask a question about indexed PDF content.

Request:

{
  "question": "What is the main conclusion?",
  "document_id": "document-id",
  "top_k": 5
}

Example response:

{
  "answer": "The main conclusion is ...",
  "sources": [
    {
      "document_id": "document-id",
      "filename": "example.pdf",
      "page_number": 4,
      "relevance_score": 0.82
    }
  ]
}
Errors

Validation errors return HTTP 422.

Not-found resources return HTTP 404.

Server errors return HTTP 500.

Interactive Documentation

FastAPI automatically provides:

/docs
/redoc

```markdown
# docs/rag_pipeline.md

# RAG Pipeline

## 1. Document Ingestion

The pipeline starts when a user uploads a PDF.

```text
PDF
 ↓
Validation
 ↓
Storage
 ↓
PDF extraction
 ↓
Text cleaning
 ↓
Chunking
 ↓
Embedding
 ↓
ChromaDB
2. PDF Extraction

The PDF service reads each page independently.

Each page produces:

document_id
page_number
text

This allows answers to be associated with the original PDF page.

3. Chunking

Large documents cannot efficiently be supplied to an LLM as one context.

The text is therefore divided into smaller overlapping chunks.

The default configuration is:

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

The overlap helps preserve context between neighboring chunks.

4. Embedding

Each chunk is converted into a vector using:

all-MiniLM-L6-v2

The vectors represent semantic meaning rather than simple keyword matching.

5. Vector Storage

ChromaDB stores:

chunk ID
document ID
document filename
page number
chunk text
embedding
metadata

Cosine similarity is used for semantic retrieval.

6. Query Processing

When a user asks a question:

Question
 ↓
Question embedding
 ↓
Vector similarity search
 ↓
Top-K chunks
 ↓
Relevance filtering

The default number of retrieved chunks is:

TOP_K = 5
7. Context Construction

Retrieved chunks are assembled into a structured context.

Each chunk contains source information so that the generated response can be associated with a document and page.

8. Generation

The context and question are sent to the configured Groq model.

The LLM is instructed to:

Use the supplied context
Avoid unsupported claims
Answer clearly
State when the context is insufficient
Avoid inventing information
9. Source Attribution

The final response contains source references.

Sources include:

document ID
filename
page number
relevance score
10. Grounding

If no sufficiently relevant chunks are found, the application does not generate an unsupported answer.

Instead, it returns a response indicating that the indexed documents do not contain enough relevant information.

Pipeline Summary
                 ┌──────────────┐
                 │     PDF      │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  Extraction  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Chunking   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  Embeddings  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  ChromaDB    │
                 └──────┬───────┘
                        │
                     Query
                        │
                        ▼
                 ┌──────────────┐
                 │  Retrieval   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  Groq LLM    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Answer +     │
                 │ Sources      │
                 └──────────────┘

```markdown
# docs/usage.md

# Usage Guide

## Requirements

Install:

- Python 3.12+
- pip
- Git
- Optional Docker

A Groq API key is required for question answering.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/pdf-question-answering-bot.git
cd pdf-question-answering-bot

Create a virtual environment:

python -m venv .venv

Windows:

.venv\Scripts\Activate.ps1

Linux/macOS:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Environment

Copy:

.env.example

to:

.env

Set:

GROQ_API_KEY=your_groq_api_key
Start the Application
uvicorn app.main:app --reload

Open:

http://localhost:8000
API Documentation

Open:

http://localhost:8000/docs
Uploading a PDF

Use the web interface or API.

Example:

curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:8000/api/v1/documents/upload
Asking Questions

Example:

curl -X POST \
  http://localhost:8000/api/v1/questions/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is this document about?\"}"
Ingesting a PDF from the Command Line
python scripts/ingest_pdf.py path/to/document.pdf
Rebuilding the Index
python scripts/rebuild_index.py
Running Tests
pytest
Running Linting
ruff check app tests scripts
black --check app tests scripts
Evaluation

Create a JSON file:

[
  {
    "question": "What is the main topic?",
    "expected_keywords": [
      "topic"
    ]
  }
]

Run:

python scripts/evaluate.py evaluation.json
Production Notes

Before production:

Configure a production CORS origin.
Use HTTPS.
Store secrets outside source control.
Use managed persistent storage.
Configure monitoring.
Configure rate limiting.
Use a production reverse proxy.

```markdown
# docs/deployment.md

# Deployment

## Docker

Build the image:

```bash
docker build -t pdf-question-answering-bot .

Run:

docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  pdf-question-answering-bot

Open:

http://localhost:8000
Docker Compose

Start:

docker compose up --build

Stop:

docker compose down
Render

The repository includes:

render.yaml

The service uses:

uvicorn app.main:app --host 0.0.0.0 --port $PORT

Set the following environment variable in Render:

GROQ_API_KEY
Persistent Storage

The application stores uploaded files and ChromaDB data locally.

For ephemeral cloud instances, persistent storage should be configured.

Production architecture should preferably use object storage for PDFs and a managed vector database for embeddings.

Environment Variables

Important variables include:

APP_ENV=production
DEBUG=false
GROQ_API_KEY=...
LLM_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PERSIST_DIRECTORY=./data/chroma
UPLOAD_DIRECTORY=./data/uploads
PROCESSED_DIRECTORY=./data/processed
Security Checklist

Before production:

[ ] DEBUG=false
[ ] Strong CORS configuration
[ ] HTTPS enabled
[ ] Secrets stored securely
[ ] Upload size limits configured
[ ] PDF validation enabled
[ ] Rate limiting enabled
[ ] Dependency auditing enabled
[ ] Persistent storage configured
[ ] Application monitoring configured
[ ] Error logging configured
Health Check

Use:

GET /health

or:

GET /api/v1/health

These endpoints can be used by deployment platforms for health monitoring.
