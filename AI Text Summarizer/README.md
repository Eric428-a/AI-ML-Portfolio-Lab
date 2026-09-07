# AI Text Summarizer

AI-powered text summarization platform built with FastAPI and
Vanilla JavaScript.

## Features

- Text summarization
- Concise, balanced and detailed modes
- Text statistics
- Compression ratio
- REST API
- Interactive frontend
- API documentation
- Automated tests
- Docker support
- Security headers
- CI/CD workflows
- Linting
- Dependency security scanning

## Architecture

```text
Browser
   |
   v
Vanilla JS Frontend
   |
   | HTTP/JSON
   v
FastAPI API
   |
   v
Summarizer Service
   |
   +----------------+
   |                |
   v                v
Text Processor   Model Service
                     |
                     v
                 AI Model

Requirements
Python 3.12+
pip
Git
Docker (optional)
Installation

Clone the repository:

git clone <repository-url>
cd ai-text-summarizer

Create a virtual environment:

python -m venv .venv

Windows:

.venv\Scripts\Activate.ps1

Linux/macOS:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create environment configuration:

Copy-Item .env.example .env

Linux/macOS:

cp .env.example .env
Run API
uvicorn app.main:app --reload

API:

http://localhost:8000

Swagger:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc
Run Frontend

Open:

frontend/index.html

The frontend communicates with:

http://localhost:8000/api/v1
API
Health
GET /health
Summarizer Health
GET /api/v1/summarizer/health
Summarize
POST /api/v1/summarizer/summarize

Example request:

{
    "text": "Artificial intelligence is changing...",
    "min_length": 30,
    "max_length": 150,
    "style": "balanced"
}
Summary Styles
Concise

Produces a shorter summary containing the most important information.

Balanced

Provides a balance between brevity and context.

Detailed

Preserves more information from the original content.

Testing
pytest -q
Linting
ruff check app tests scripts
Formatting
ruff format app tests scripts
Security Audit
pip-audit
Docker

Build:

docker compose build

Start:

docker compose up

Stop:

docker compose down
Environment

Important variables:

MODEL_PROVIDER=local
MODEL_NAME=facebook/bart-large-cnn
MAX_INPUT_CHARACTERS=100000
DEFAULT_MAX_LENGTH=150
DEFAULT_MIN_LENGTH=30

External AI providers can be integrated through the model service
abstraction.

Project Structure
ai-text-summarizer/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── lint.yml
│       └── security.yml
│
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── data/
├── docs/
├── frontend/
├── models/
├── scripts/
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md                 