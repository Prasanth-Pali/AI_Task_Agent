# 🤖 AI Task Management Agent

An AI-powered task management application that uses natural language to interact with task records. Built with Python, LangChain, Groq LLM, FastAPI, SQLAlchemy, and Microsoft SQL Server.

The application connects an LLM to real backend APIs through LangChain tools, enabling users to retrieve, create, update, and delete tasks using natural-language requests.

## ✨ Features

- 🧠 **LLM Integration** — Uses Groq to understand user requests and generate responses.
- 🛠️ **LangChain Tool Calling** — Connects AI reasoning to Python functions and backend APIs.
- 📋 **Task Retrieval** — Retrieve task records and filter them by status.
- ➕ **Create Tasks** — Create tasks through natural-language requests.
- ✏️ **Update Tasks** — Update task details or status.
- 🗑️ **Delete Tasks** — Delete tasks by ID.
- 🚀 **REST APIs** — FastAPI provides endpoints for task operations.
- 🗄️ **SQL Server Integration** — Store and retrieve task data using SQLAlchemy.
- ✅ **Request Validation** — Validate task input using Pydantic schemas.
- 🔐 **Environment Configuration** — Keep API keys and sensitive configuration outside source control.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and AI agent logic |
| LangChain | Agent orchestration and tool calling |
| Groq LLM | Natural-language understanding and responses |
| FastAPI | REST API development |
| SQLAlchemy | Database connectivity and ORM |
| Microsoft SQL Server | Task data storage |
| Pydantic | Input validation and schemas |
| Requests | HTTP communication with the backend API |
| Uvicorn | Runs the FastAPI application |
| python-dotenv | Loads environment variables |

## 🏗️ Architecture

```text
User
  |
  v
LangChain Agent / LLM
  |
  v
Selects a Tool
  |
  v
Python @tool Function
  |
  v
FastAPI REST API
  |
  v
SQLAlchemy
  |
  v
Microsoft SQL Server
  |
  v
API Result -> LLM -> User Response
```

The LLM interprets the user's request and can select an appropriate tool. The tool calls the FastAPI backend, which retrieves or modifies database records. The agent uses the returned result to formulate its response.

## 📁 Project Structure

```text
AI-Task-Management-Agent/
│
├── .venv/                 # Local Python environment (not committed)
│
├── app/
│   ├── __pycache__/       # Generated Python cache (not committed)
│   ├── __init__.py
│   ├── database.py        # SQLAlchemy database connection
│   ├── dependencies.py    # FastAPI database dependencies
│   ├── llm.py             # LLM / agent logic
│   ├── main.py            # FastAPI application and task APIs
│   ├── models.py          # Database-first SQLAlchemy models
│   ├── schemas.py         # Pydantic request schemas
│   └── tools.py           # LangChain tools for task operations
│
├── .env                   # Local secrets (not committed)
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Prerequisites

- Python 3.11 or another version supported by the installed dependencies.
- Microsoft SQL Server.
- Microsoft ODBC Driver 18 for SQL Server, or the driver configured in your application.
- A Groq API key.
- Git.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Prasanth-Pali/AI-Task-Management-Agent.git
cd AI-Task-Management-Agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the environment

Create a `.env` file in the project root and configure your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own key. Never commit your real `.env` file.

### 5. Configure SQL Server

Configure the connection settings in `app/database.py` for your local SQL Server instance and database.

The project uses a database-first approach. The existing database schema is the source of truth, and the SQLAlchemy models in `app/models.py` are generated from the existing database.

Ensure the database and `Tasks` table exist before starting the backend.

### 6. Start the FastAPI backend

From the project root, run:

```bash
uvicorn app.main:app --reload
```

The API runs at:

- Base URL: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`

Keep this terminal running.

### 7. Run the AI agent

Open a second terminal, activate the virtual environment, and run:

```powershell
python -m app.llm
```

This assumes `app/llm.py` contains a runnable entry point. If the file uses a different execution pattern, use the command appropriate to its implementation.

## 🔌 REST API Endpoints

The core task operations are:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tasks` | Retrieve all tasks |
| GET | `/api/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/api/tasks` | Create a task |
| PATCH | `/api/tasks/{task_id}` | Update selected task fields |
| DELETE | `/api/tasks/{task_id}` | Delete a task |

If the optional PUT endpoint remains in your backend, it can also be used to replace a task's editable fields.

### Supported task statuses

- `Pending`
- `InProgress`
- `Completed`

### Example request: Create a task

**POST** `/api/tasks`

```json
{
  "title": "Learn LangChain tools",
  "description": "Connect AI tools to task APIs",
  "dueDateUtc": "2026-10-30T12:00:00",
  "status": "Pending"
}
```

## 💬 Example Natural-Language Requests

- "Show me all tasks."
- "Give me the tasks whose status is Completed."
- "Show me task 1."
- "Create a task to learn Azure."
- "Mark task 3 as Completed."
- "Change the title of task 2."
- "Delete task 5."

For task-related questions, the agent should retrieve the real task data through the backend tools instead of inventing records.

## 🔐 Security

- Keep API keys and database credentials in environment variables.
- Never commit `.env` or other secret files.
- Add `.env`, `.venv/`, and `__pycache__/` to `.gitignore`.
- Validate incoming API requests.
- Handle API and database errors safely.
- Add authentication and authorization before exposing the application to external users.
- Treat delete operations as destructive actions.

## 🛣️ Future Enhancements

- Angular chat interface.
- User authentication and role-based access control.
- Due-date reminders and overdue task detection.
- Conversation memory.
- Retrieval-Augmented Generation (RAG).
- Docker containerization.
- GitHub Actions CI/CD.
- Azure deployment and monitoring.
- Automated unit and integration tests.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- LLM integration using Groq.
- LangChain agents and custom tools.
- AI tool calling and REST API integration.
- FastAPI backend development.
- SQL Server access with SQLAlchemy.
- Pydantic validation and error handling.
- Environment-based configuration.
- Git and GitHub workflows.

## 👨‍💻 Author

**Prasanth Pali**

GitHub: [Prasanth-Pali](https://github.com/Prasanth-Pali)

---

*Built to explore practical AI agents, tool calling, and backend integration.*
