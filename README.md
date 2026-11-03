# 🤖 AI Task Agent

An AI-powered task management application that allows users to manage their tasks using natural language. Instead of manually navigating through forms or endpoints, users can interact with an AI agent to create, retrieve, update, and delete tasks through conversational commands.

Built using **Python, FastAPI, LangChain, Groq LLM, Angular, and Microsoft SQL Server**, this project demonstrates how LLM-powered agents can interact with real-world backend APIs and databases using tool calling.

## ✨ Key Features

- 🧠 **AI-Powered Conversations** – Interact with the application using natural language.
- 🤖 **AI Agent Integration** – Uses LangChain agents to understand requests and decide which tools to execute.
- 🛠️ **Tool Calling** – Connects AI reasoning with actual backend API operations.
- 📋 **Task Retrieval** – Retrieve all tasks and access individual task details.
- ➕ **Task Creation** – Create new tasks through conversational instructions.
- ✏️ **Task Updates** – Modify existing task details and status.
- 🗑️ **Task Deletion** – Delete tasks using natural-language commands.
- 💬 **Angular Chat Interface** – User-friendly conversational interface.
- ⚡ **RESTful APIs** – FastAPI handles backend operations.
- 🗄️ **SQL Server Integration** – Persistent task storage using SQLAlchemy.
- ✅ **Data Validation** – Pydantic schemas for request validation.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | AI agent and backend development |
| LangChain | Agent orchestration and tool calling |
| Groq LLM | Natural-language understanding |
| FastAPI | REST API development |
| Angular | Frontend and chat interface |
| TypeScript | Frontend application logic |
| SQL Server | Relational database |
| SQLAlchemy | ORM and database connectivity |
| Pydantic | Data validation |
| Uvicorn | ASGI application server |
| Git & GitHub | Version control |

## 🏗️ System Architecture

              User
               |
               v
       Angular Chat Interface
               |
               v
          FastAPI Backend
               |
               v
        LangChain AI Agent
               |
               v
          Groq LLM
               |
       Understands Intent
               |
               v
       Selects Appropriate Tool
               |
               v
       Python Tool Functions
               |
               v
         REST API Calls
               |
               v
           SQLAlchemy
               |
               v
        Microsoft SQL Server
               |
               v
         API Response
               |
               v
       AI Agent Processes Result
               |
               v
       Natural Language Response
               |
               v
             User

### 🔄 How It Works

1. The user enters a task-related instruction in the Angular chat interface.
2. The request is sent to the FastAPI backend.
3. The LangChain agent uses the Groq LLM to understand the user's intent.
4. Based on the request, the agent selects the appropriate tool.
5. The selected Python tool communicates with the backend REST API.
6. FastAPI performs the required database operation using SQLAlchemy.
7. SQL Server returns the operation result.
8. The agent processes the result and generates a natural-language response.
9. The response is displayed in the Angular chat interface.

## 📁 Project Structure

AI_Task_Agent/
│
├── Backend/
│   ├── __init__.py
│   ├── database.py
│   ├── DB_Script/
│   ├── llm.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── tools.py
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── assets/
│   │   └── environments/
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── .env
├── .gitignore
└── README.md

## ⚙️ Prerequisites

Make sure you have installed:

- Python 3.11+
- Node.js and npm
- Angular CLI
- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- Groq API Key

## 🚀 Installation and Setup

### 1. Clone the Repository

git clone https://github.com/Prasanth-Pali/AI_Task_Agent.git

cd AI_Task_Agent

### 2. Backend Setup

Navigate to the backend directory:

cd Backend

Create a virtual environment:

python -m venv .venv


Activate the environment on Windows:


.venv\Scripts\activate


Install dependencies:


pip install -r requirements.txt


### 3. Configure Environment Variables

Create a `.env` file inside the Backend directory.


GROQ_API_KEY=your_groq_api_key


Configure your SQL Server connection string in the database configuration.

Make sure your database and required tables are created before starting the application.

### 4. Start the Backend


uvicorn app.main:app --reload


Backend URL:


http://127.0.0.1:8000


Swagger API Documentation:


http://127.0.0.1:8000/docs


### 5. Frontend Setup

Open another terminal and navigate to the frontend directory:


cd Frontend


Install dependencies:


npm install


Start the Angular development server:


ng serve


Open the application:


http://localhost:4200


## 🔌 Core API Operations

The application supports the following task management operations:

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks` | Retrieve all tasks |
| GET | `/api/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/api/tasks` | Create a new task |
| PATCH | `/api/tasks/{task_id}` | Update an existing task |
| DELETE | `/api/tasks/{task_id}` | Delete a task |

*Note: These are the documented core backend operations. Refer to the FastAPI Swagger documentation for the actual implemented routes and request schemas.*

## 💬 Example AI Commands

Users can interact with the AI agent using instructions such as:


Show me all tasks.

Get all pending tasks.

Create a task to learn Azure DevOps.

Update task 3 and mark it as Completed.

Delete task 5.

Show me the details of task 2.


The agent interprets the request, selects the appropriate tool, and executes the corresponding operation through the backend.

## 🗄️ Database

The application uses **Microsoft SQL Server** for persistent task storage.

- Database: `AITaskAssistantDB`
- ORM: SQLAlchemy
- Database approach: Database First
- Data validation: Pydantic

SQLAlchemy models are mapped to the existing database schema.

## 🔐 Configuration and Security

- Store API keys and database credentials in environment variables.
- Exclude `.env` and virtual environment folders from Git.
- Validate incoming requests using Pydantic.
- Handle API and database errors appropriately.
- Configure CORS to allow communication between Angular and FastAPI.

## 🎯 Key Concepts Demonstrated

This project demonstrates practical implementation of:

- Large Language Model (LLM) integration.
- AI agents and agent orchestration.
- LangChain tool calling.
- Natural-language-to-action workflows.
- REST API integration with AI agents.
- FastAPI backend development.
- Angular frontend development.
- SQL Server database integration.
- SQLAlchemy ORM and database-first development.
- Pydantic data validation.
- Full-stack application architecture.

## 👨‍💻 Author

**Prasanth Pali**

- GitHub: https://github.com/Prasanth-Pali

---

⭐ If you find this project interesting, consider giving it a star!

**Built to explore practical AI agents, LLM tool calling, and full-stack application development.**