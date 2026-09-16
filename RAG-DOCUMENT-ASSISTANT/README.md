# RAG Document Assistant

A document-based Retrieval-Augmented Generation (RAG) application for uploading documents, processing their contents, creating embeddings, retrieving relevant document chunks, and answering questions using retrieved context.

---

## Features

- PDF document loading
- DOCX document loading
- TXT document loading
- Document upload API
- Document metadata storage
- Text chunking
- Sentence Transformer embeddings
- Local JSON vector store
- Semantic document retrieval
- LLM-powered question answering
- Source references for answers
- FastAPI backend
- Browser-based frontend
- Automated tests
- PowerShell development runner

---

## Project Structure

```text
RAG-DOCUMENT-ASSISTANT/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── app.py
│   ├── startup.py
│   ├── shutdown.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── documents.py
│   │       ├── chat.py
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── document.py
│   │   ├── chat.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   └── chat_service.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── parser.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   └── pipeline.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py
│       └── text_utils.py
│
├── data/
│   ├── documents/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── uploads/
│       └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_documents.py
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   └── test_chat.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── documents.js
│       └── chat.js
│
├── scripts/
│   ├── ingest.py
│   └── rebuild_index.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.ps1


#Architecture
                    ┌─────────────────────┐
                    │      Frontend       │
                    │  HTML / CSS / JS    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       REST API      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │  Documents  │  │    Chat     │  │   Health    │
       │     API     │  │     API     │  │     API     │
       └──────┬──────┘  └──────┬──────┘  └─────────────┘
              │                │
              ▼                ▼
       ┌─────────────┐  ┌─────────────┐
       │  Ingestion  │  │ Retrieval   │
       │   Service   │  │   Service   │
       └──────┬──────┘  └──────┬──────┘
              │                │
              ▼                ▼
       ┌─────────────┐  ┌─────────────┐
       │   Parser    │  │Vector Store │
       │  + Chunker  │  │  + Search   │
       └──────┬──────┘  └──────┬──────┘
              │                │
              ▼                ▼
       ┌─────────────┐  ┌─────────────┐
       │  Embedding  │  │  Retrieved  │
       │    Model    │  │   Context   │
       └─────────────┘  └──────┬──────┘
                               │
                               ▼
                       ┌─────────────┐
                       │     LLM     │
                       └──────┬──────┘
                              │
                              ▼
                       Answer + Sources



#RAG Pipeline

The application follows this general flow:
RAG Pipeline

The application follows this general flow:
Upload
   ↓
Parse
   ↓
Clean
   ↓
Chunk
   ↓
Embed
   ↓
Store vectors
   ↓
Receive question
   ↓
Embed question
   ↓
Semantic retrieval
   ↓
Retrieve relevant chunks
   ↓
Build prompt
   ↓
LLM
   ↓
Answer + sources



Requirements

The project requires:

Python 3.11+
Windows, Linux, or macOS
Internet connection for downloading the embedding model during first use
OpenAI API key for LLM-powered answers
Installation
1. Create the Virtual Environment

From the project root:

python -m venv .venv
2. Activate the Virtual Environment

On Windows PowerShell:

.\.venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
Environment Configuration

The project uses environment variables stored in .env.

Copy the example configuration into your local .env file.

Example:

APP_NAME=RAG Document Assistant
APP_VERSION=1.0.0
ENVIRONMENT=development

API_PREFIX=/api/v1

HOST=127.0.0.1
PORT=8000

LOG_LEVEL=INFO

UPLOAD_DIR=data/uploads
DOCUMENT_DIR=data/documents
PROCESSED_DIR=data/processed

MAX_UPLOAD_SIZE_MB=25

DATABASE_URL=sqlite:///./data/rag_assistant.db

VECTOR_STORE_PATH=data/processed/vector_store

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=

CHUNK_SIZE=800
CHUNK_OVERLAP=120
RETRIEVAL_TOP_K=5

Set your API key:

OPENAI_API_KEY=your_api_key_here

Do not commit your real .env file to GitHub.

Running the Application
Windows PowerShell

The easiest method is:

.\run.ps1

The PowerShell script:

Locates the project root
Creates the virtual environment if necessary
Activates the virtual environment
Updates pip
Installs requirements
Creates required data directories
Starts the FastAPI server
Manual Startup

You can also start the application manually:

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

The backend will be available at:

http://127.0.0.1:8000

FastAPI interactive documentation:

http://127.0.0.1:8000/docs

Alternative documentation:

http://127.0.0.1:8000/redoc
API
Health Check
Request
GET /api/v1/health
Example
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health

Expected response structure:

{
    "status": "ok",
    "application": "RAG Document Assistant",
    "version": "1.0.0",
    "timestamp": "2026-01-01T00:00:00+00:00"
}
List Documents
Request
GET /api/v1/documents
PowerShell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/documents
Response
{
    "documents": [],
    "total": 0
}
Upload Document
Request
POST /api/v1/documents/upload

Supported file types:

.pdf
.docx
.txt
PowerShell Example
$form = @{
    file = Get-Item ".\example.pdf"
}

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/documents/upload" `
    -Method Post `
    -Form $form

The uploaded document is stored under:

data/uploads/
Chat
Request
POST /api/v1/chat
Example Request
{
    "question": "What is this document about?",
    "document_ids": [],
    "top_k": 5
}
Example PowerShell Request
$body = @{
    question = "What is this document about?"
    document_ids = @()
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
Document Processing

Documents move through the following processing stages:

Document Upload
       ↓
File Validation
       ↓
File Storage
       ↓
Document Parsing
       ↓
Text Extraction
       ↓
Text Chunking
       ↓
Embedding Generation
       ↓
Vector Storage
       ↓
Semantic Retrieval
Supported Documents
PDF

PDF files are processed using pypdf.

.pdf
DOCX

Microsoft Word documents are processed using python-docx.

.docx
TXT

Plain text documents are loaded directly.

.txt
Chunking

The RAG system divides extracted document text into smaller chunks before creating embeddings.

Default configuration:

CHUNK_SIZE=800
CHUNK_OVERLAP=120

Chunking allows the retrieval system to search smaller sections of documents instead of processing an entire document as one large context.

Embeddings

The project uses:

sentence-transformers/all-MiniLM-L6-v2

The embedding model converts document chunks into numerical vectors.

The same embedding process is used for user questions.

The system then compares the question vector with document vectors to identify semantically relevant chunks.

Vector Store

The initial implementation uses a local JSON-based vector store.

The index is stored under:

data/processed/vector_store/

The primary index file is:

data/processed/vector_store/index.json

Each stored record contains information such as:

Vector ID
Document ID
Chunk Index
Text
Embedding
Retrieval

When a user asks a question:

Question
   ↓
Question Embedding
   ↓
Vector Similarity Search
   ↓
Top-K Relevant Chunks
   ↓
Document Context

The default number of retrieved chunks is:

RETRIEVAL_TOP_K=5

This can be changed through .env.

LLM

The current LLM configuration uses:

LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini

The LLM receives the retrieved document context together with the user's question.

The prompt instructs the model to:

Use the supplied document context
Avoid inventing information
Clearly state when the answer cannot be found
Keep the response relevant to the question

If no API key is configured, the current implementation does not make an external LLM request.

Source References

The chat response includes source information for retrieved chunks.

Each source can contain:

Document ID
Filename
Chunk Index
Page Number
Content

This allows the application to show which document sections contributed to the retrieved context.

Database

The initial database is SQLite.

Configuration:

DATABASE_URL=sqlite:///./data/rag_assistant.db

Database file:

data/rag_assistant.db

The database stores document metadata and document chunks.

Data Directories

The project uses three main data directories.

Uploads
data/uploads/

Contains uploaded files.

Documents
data/documents/

Reserved for document-related application storage.

Processed
data/processed/

Contains processed application data and vector indexes.

Ingestion Script

Uploaded documents can be processed using:

python scripts/ingest.py

The ingestion process:

Document
   ↓
Load
   ↓
Parse
   ↓
Chunk
   ↓
Embed
   ↓
Store vectors
   ↓
Save chunks
Rebuild Vector Index

If the vector index needs to be recreated:

python scripts/rebuild_index.py

This rebuilds the local vector index using stored document chunks.

Testing

The project includes tests for:

Health API
Document API
Document loading
Text chunking
Retrieval utilities
Chat API validation

Run all tests:

pytest

Run tests with detailed output:

pytest -v

Run a specific test file:

pytest tests/test_health.py -v

Run the document tests:

pytest tests/test_documents.py -v

Run ingestion tests:

pytest tests/test_ingestion.py -v

Run retrieval tests:

pytest tests/test_retrieval.py -v

Run chat tests:

pytest tests/test_chat.py -v
Frontend

The project includes a browser frontend built with:

HTML
CSS
JavaScript

Frontend structure:

frontend/
│
├── index.html
│
├── css/
│   └── style.css
│
└── js/
    ├── app.js
    ├── documents.js
    └── chat.js
index.html

Contains the main application interface.

style.css

Contains the application styling.

app.js

Handles:

Global application state
API requests
Health status
Common UI utilities
documents.js

Handles:

Document loading
Document rendering
File uploads
Document selection
chat.js

Handles:

Chat messages
Question submission
Retrieved sources
Chat clearing
Loading states
Security

Do not commit API keys or other secrets.

The .gitignore excludes:

.env

Database files are also excluded:

*.db
*.sqlite
*.sqlite3

Uploaded and processed data are excluded:

data/uploads/*
data/processed/*

The project should be further hardened before production deployment.

Potential future security improvements include:

Authentication
Authorization
User-specific document ownership
File content validation
Rate limiting
Request size controls
Secure secret management
Audit logging
Access control
Production HTTPS
Development Workflow

Recommended development workflow:

1. Create virtual environment
        ↓
2. Install dependencies
        ↓
3. Configure .env
        ↓
4. Start FastAPI
        ↓
5. Test health endpoint
        ↓
6. Upload document
        ↓
7. Ingest document
        ↓
8. Build embeddings
        ↓
9. Query document
        ↓
10. Inspect retrieved sources
        ↓
11. Run tests
        ↓
12. Improve system
Example Development Session

Create and activate the environment:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the backend:

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

Open:

http://127.0.0.1:8000/docs

Upload a document through the API documentation.

Then run:

python scripts/ingest.py

Finally, send a question through:

POST /api/v1/chat
Design Principles

The project is organized around separation of responsibilities.

API Layer

Responsible for:

HTTP requests
HTTP responses
Validation
Routing

Location:

app/api/
Service Layer

Responsible for:

Business logic
Document operations
Chat operations
Retrieval operations

Location:

app/services/
RAG Layer

Responsible for:

Loading
Parsing
Chunking
Embeddings
Vector search
Retrieval
Prompt construction

Location:

app/rag/
Database Layer

Responsible for:

Document metadata
Document chunks
Persistence

Location:

app/db/
Schema Layer

Responsible for:

Request validation
Response validation
API data models

Location:

app/schemas/
Current Technology Stack
Component	Technology
Backend	FastAPI
API Server	Uvicorn
Language	Python
Database	SQLite
ORM	SQLAlchemy
PDF Processing	pypdf
DOCX Processing	python-docx
Embeddings	Sentence Transformers
Vector Storage	Local JSON
LLM	OpenAI API
Frontend	HTML / CSS / JavaScript
Testing	Pytest
Configuration	Pydantic Settings
Development OS	Windows PowerShell
Future Architecture Improvements

The current implementation is intentionally simple and can be expanded.

Potential improvements include:

Authentication
User
 ↓
Authentication
 ↓
Authorization
 ↓
Documents

Possible future functionality:

User registration
Login
Sessions
JWT authentication
User-specific documents
Persistent Vector Database

The local JSON vector store can eventually be replaced with a dedicated vector database.

Possible options:

Qdrant
Chroma
FAISS
pgvector

The existing service-oriented architecture makes this replacement easier.

Background Processing

Large documents can eventually be processed asynchronously:

Upload
   ↓
Job Queue
   ↓
Background Worker
   ↓
Parsing
   ↓
Chunking
   ↓
Embedding
   ↓
Indexing

This prevents long ingestion operations from blocking API requests.

Streaming Responses

The chat system can later support streaming responses:

User Question
      ↓
Retrieval
      ↓
LLM
      ↓
Token 1
Token 2
Token 3
Token 4
...

This can improve the interactive experience for longer responses.

Better Retrieval

Future retrieval improvements can include:

Hybrid search
Keyword search
Semantic search
Reranking
Metadata filtering
Query expansion
Multiple retrieval strategies
Better similarity thresholds
Better Document Parsing

Future document support can include:

PDF
DOCX
TXT
CSV
XLSX
PPTX
HTML
Markdown
Images
Scanned documents

OCR can eventually be added for scanned documents.

Production Considerations

Before production deployment, the system should be reviewed for:

Authentication
Authorization
Secure file handling
Database migrations
Persistent vector storage
Background jobs
Logging
Monitoring
Error tracking
Rate limiting
HTTPS
Secret management
Backup and recovery
Scalability
Multi-user isolation

The current project is primarily structured as a development foundation.

License

Add the project's chosen license here before public distribution.

Example:

MIT License

or another license appropriate for the project.

Project Status

Current implementation includes:

FastAPI application
REST API
Document upload
Document metadata
PDF parsing
DOCX parsing
TXT parsing
Text chunking
Embedding generation
Local vector storage
Semantic retrieval
RAG prompt construction
LLM integration
Chat endpoint
Source references
Frontend interface
Test suite
Ingestion script
Vector index rebuild script
Environment configuration
PowerShell startup script
Roadmap
Phase 1
├── Backend foundation
├── Configuration
├── Database
├── Schemas
├── Services
└── RAG foundation

Phase 2
├── Frontend
├── Document interface
└── Chat interface

Phase 3
├── Automated tests
└── Documentation

Next Development Stages
├── Stabilization
├── Database relationship fixes
├── Automatic ingestion
├── Static frontend serving
├── Improved retrieval
├── Better source tracking
├── Authentication
├── Persistent vector database
├── Background processing
└── Production deployment
Author

RAG Document Assistant

Built as a modular document intelligence and Retrieval-Augmented Generation application.