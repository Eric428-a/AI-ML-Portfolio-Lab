# Multi-Document RAG System — Frontend

React, TypeScript, Vite, and TanStack Query frontend for the
Multi-Document RAG System.

## Requirements

- Node.js 20+
- npm
- Running FastAPI backend

## Installation

```powershell
npm install
```

## Environment

Create `.env` from `.env.example`.

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
VITE_API_KEY=
VITE_APP_NAME=Document Intelligence
```

## Development

```powershell
npm run dev
```

Open:

http://127.0.0.1:5173

## Production build

```powershell
npm run typecheck
npm run build
npm run preview
```

Production files are generated in `dist/`.

## Features

- Workspace dashboard and document statistics
- Multi-file upload interface
- PDF, DOCX, TXT, Markdown, and CSV support
- Document library with grid and table views
- Processing status and document metadata
- Knowledge-base and collection management
- AI chat interface
- Conversation history
- Retrieved source citations
- Expandable citation excerpts
- Markdown-rendered AI answers
- Backend connection status
- Responsive layouts
- Searchable workspace navigation

## Backend

The frontend expects the FastAPI service at:

`http://127.0.0.1:8000/api/v1`

The backend must allow the frontend origin through its CORS configuration.

## Authentication

The login page is currently a presentation interface. Actual user
authentication, session management, and authorization must be implemented
and enforced by the backend before the application is deployed publicly.

## Deployment

Build the frontend using `npm run build`, or build the included Dockerfile.

Configure the production API URL at build time using `VITE_API_BASE_URL`.

Do not put provider API secrets in frontend environment variables.
Variables prefixed with `VITE_` are exposed to browser code.