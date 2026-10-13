# Multi-Document RAG System

A full-stack Retrieval-Augmented Generation application for uploading documents, organizing document collections, searching document content, and asking questions grounded in retrieved passages.

## Features

- Upload and manage supported documents.
- Parse documents and split text into overlapping chunks.
- Generate vector embeddings.
- Store and retrieve document vectors.
- Retrieve relevant passages for user questions.
- Optionally rerank retrieved passages.
- Generate answers using a configured language model.
- Return source citations with chat responses.
- Organize documents into collections.
- Provide a React and TypeScript frontend.
- Run locally or with Docker Compose.

## Project Structure

```text
Multi-Document-RAG-System/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml
├── .env.example
└── .gitignore




## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- npm
- An API key for the configured LLM provider if using a hosted model
- Docker Desktop for containerized deployment
Backend Setup
Open a terminal in the project root.

1. Enter the backend directory
cd backend


2. Create a virtual environment
Windows PowerShell:
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1


Windows Command Prompt:
py -3.11 -m venv .venv
.venv\Scripts\activate.bat


Linux or macOS:
python3 -m venv .venv
source .venv/bin/activate


3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt


4. Configure environment variables
Create backend/.env and configure the required variables using backend/.env.example as a reference.
Never commit API keys, passwords, or production secrets.

5. Start the API
From the backend directory:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


API base URL:
http://127.0.0.1:8000


Swagger documentation:
http://127.0.0.1:8000/docs


ReDoc documentation:
http://127.0.0.1:8000/redoc


## Frontend Setup

Open another terminal.
1. Enter the frontend directory
cd frontend


2. Install dependencies
npm install


3. Configure the frontend API URL
Create frontend/.env with the API URL expected by the frontend configuration.
Example:
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1


Ensure this variable matches the name used by src/api/client.ts.
4. Start the development server
npm run dev


Open the local URL printed by Vite, usually:
http://localhost:5173


Running Tests
From the backend directory with the virtual environment activated:
pytest -v


Docker Deployment
Create and configure backend/.env before starting the containers.
From the project root:
docker compose up --build


Frontend:
http://localhost:8080


Backend API:
http://localhost:8000


Stop the services:
docker compose down


Stop services and remove persisted Docker volumes:
docker compose down -v


Warning: The final command permanently deletes data stored in the Compose-managed volumes.
Supported Document Formats
The configured upload allowlist is:
- PDF
- DOCX
- TXT
- Markdown
- CSV

Actual parsing support depends on the installed parser dependencies and the implemented file parser.
Security Notes
- Keep .env files out of version control.
- Replace development secrets before deployment.
- Validate file extensions, MIME types, and file sizes on the server.
- Do not expose internal upload directories as public static assets.
- Add authentication and authorization before exposing private documents to multiple users.
- Configure production CORS origins explicitly.
- Protect API endpoints with rate limits and request validation.
- Treat document contents as untrusted input.
- Avoid placing confidential document contents in application logs.
- Configure persistent, backed-up storage for production deployments.

Important Implementation Notes
- SQLite is suitable for local development; production database requirements may differ.
- Embedding and reranking models may download model files on first use.
- Hosted LLM requests may incur provider charges.
- Retrieval quality depends on chunking, embeddings, document parsing, and ranking.
- Citations should reference retrieved source passages rather than unsupported claims.
- Configure consistent collection identifiers between ingestion and retrieval.

##License
Add the license appropriate to your project before publishing or distributing it.
