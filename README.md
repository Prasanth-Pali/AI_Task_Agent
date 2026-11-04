# AI Task Agent

AI Task Agent is a full-stack task management application that combines an Angular frontend, a FastAPI backend, and a LangChain-powered AI assistant. Users can manage tasks through a chat interface or by calling the REST API directly. The system uses PostgreSQL for persistence and Groq for LLM inference.

## Overview

This project allows users to:

- create, update, view, and delete tasks
- use natural-language prompts to interact with the AI agent
- retrieve task data from PostgreSQL through a FastAPI API
- operate the frontend and backend in a single local or containerized environment

## Tech Stack

- Frontend: Angular 17, TypeScript, HTML, CSS
- Backend: FastAPI, SQLAlchemy, Pydantic
- AI: LangChain, LangChain Groq
- Database: PostgreSQL
- Runtime: Python 3.12, Node.js 20
- Containerization: Docker, Docker Compose

## Project Structure

```text
AI_Task_Agent/
├── Backend/
│   ├── __init__.py
│   ├── database.py
│   ├── llm.py
│   ├── main.py
│   ├── migrate_data.py
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
│   └── tools.py
├── Frontend/
│   ├── angular.json
│   ├── package.json
│   ├── src/
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.spec.json
│   └── ...
├── .dockerignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md
└── .gitignore
```

## Features

- AI-powered chat assistant for task operations
- CRUD endpoints for tasks
- PostgreSQL-backed data storage
- Angular frontend with task history and chat session support
- FastAPI Swagger API documentation
- Dockerized setup for local development and deployment

## Application Flow

```mermaid
flowchart LR
    User --> Frontend
    Frontend -->|HTTP| Backend
    Backend --> AI_Agent
    AI_Agent --> Groq
    AI_Agent --> Tools
    Tools --> Backend
    Backend --> PostgreSQL
```

## Environment Variables

Create a `.env` file in the project root before starting the app locally or with Docker.

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql+psycopg://username:password@host:5432/database_name
```

You can copy the provided example file:

```bash
cp .env.example .env
```

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+ or 20+
- npm
- PostgreSQL database
- Groq API key

### 1. Backend setup

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install backend packages:

```bash
pip install -r Backend/requirements.txt
```

### 2. Frontend setup

```bash
cd Frontend
npm install
```

### 3. Start the backend

From the project root:

```bash
uvicorn Backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 4. Start the frontend

In a second terminal:

```bash
cd Frontend
npm start
```

Open:

- Frontend: http://localhost:4200

## Running with Docker

The project includes a root `Dockerfile` and `docker-compose.yml` for a full-stack setup.

### Option 1: Use Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Then open:

- Frontend: http://localhost:4200
- Backend: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### Option 2: Build and run the container manually

```bash
docker build -t ai-task-agent .
docker run --env-file .env -p 8000:8000 -p 4200:4200 ai-task-agent
```

## API Endpoints

The backend exposes task and AI endpoints.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a task |
| PATCH | `/api/tasks/{task_id}` | Update a task |
| DELETE | `/api/tasks/{task_id}` | Delete a task |
| POST | `/api/chat` | Ask the AI assistant a task-related question |

## Notes

- The Angular app expects the backend to run on port 8000 during local development.
- The Docker container serves the built Angular app on port 4200 and the FastAPI backend on port 8000.
- Do not commit your `.env` file with real credentials.

## Author

Prasanth Pali