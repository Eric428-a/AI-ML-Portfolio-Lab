# AI Text Summarizer Architecture

## Overview

The application uses a layered architecture.

```text
Frontend
   |
   v
FastAPI
   |
   v
API Routes
   |
   v
Schemas
   |
   v
Summarizer Service
   |
   +---- Text Processor
   |
   +---- Model Service

Backend

The backend is organized into:

api - HTTP routes
core - application configuration and security
schemas - request and response validation
services - business and model logic
utils - reusable text and validation utilities
Frontend

The frontend uses:

HTML
CSS
Vanilla JavaScript
ES modules
Fetch API

No React, Vite, or Tailwind is required.

Summarization Pipeline
Input
  ↓
Validation
  ↓
Normalization
  ↓
Sentence extraction
  ↓
Word-frequency analysis
  ↓
Sentence scoring
  ↓
Style-based selection
  ↓
Length enforcement
  ↓
Summary response
API

Primary endpoint:

POST /api/v1/summarizer/summarize

Health endpoint:

GET /api/v1/summarizer/health
Deployment

The application can run:

Locally with Uvicorn
Inside Docker
As a FastAPI application behind a production ASGI server

### `docs/api.md`
```markdown
# API Reference

## Health

### Request

```http
GET /health
Response
{
  "status": "healthy",
  "service": "AI Text Summarizer",
  "version": "1.0.0"
}
Summarizer Health
Request
GET /api/v1/summarizer/health
Response
{
  "status": "healthy",
  "provider": "local",
  "model": "extractive-summarizer-v1"
}
Summarize
Request
POST /api/v1/summarizer/summarize
Content-Type: application/json
Body
{
  "text": "Your long text goes here...",
  "min_length": 30,
  "max_length": 150,
  "style": "balanced"
}
Styles
concise
balanced
detailed
Response
{
  "summary": "Generated summary...",
  "original_character_count": 1000,
  "summary_character_count": 350,
  "original_word_count": 180,
  "summary_word_count": 60,
  "compression_ratio": 0.3333,
  "style": "balanced",
  "model": "extractive-summarizer-v1"
}

### `docs/usage.md`
```markdown
# Usage

## Install

Create a virtual environment:

```bash
python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Configuration

Copy:

.env.example

to:

.env

Adjust values when necessary.

Run
uvicorn app.main:app --reload

Open:

http://localhost:8000

API documentation:

http://localhost:8000/docs
Test
pytest
Evaluate
python scripts/evaluate.py
Docker

Build:

docker compose build

Run:

docker compose up

Open:

http://localhost:8000
Keyboard Shortcut

Press:

Ctrl + Enter

or on macOS:

Cmd + Enter

to generate a summary.   