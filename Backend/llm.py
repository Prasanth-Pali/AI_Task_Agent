
from pathlib import Path
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from Backend.tools import (
    get_all_tasks,
    create_task,
    update_task,
    delete_task,
)

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


# Structured response model
class AIResponse(BaseModel):
    answer: str = Field(
        description="Complete user-friendly Markdown response"
    )

    summary: str = Field(
        description="Short summary of the operation"
    )

# Store conversation history in memory
checkpointer = InMemorySaver()

# Create AI Agent
agent = create_agent(
    model=llm,
    tools=[
        get_all_tasks,
        create_task,
        update_task,
        delete_task,
    ],

    system_prompt="""
You are an AI Task Management Assistant.

Help users manage their tasks using the available tools.

========================
TOOL INSTRUCTIONS
========================

1. GET ALL TASKS:

- Whenever the user asks to show, list, view, or retrieve tasks,
  you MUST call get_all_tasks.
- Display actual task records returned by the tool.
- Include Task ID, Title, Description, Status, and Due Date
  whenever available.
- If no tasks are found, tell the user clearly.
- Never invent task information.

2. CREATE TASK:

- Use create_task when the user wants to create a task.
- Task title is mandatory.
- If title is missing, ask the user.
- Use only information provided by the user.
- Check the tool result before confirming success.

3. UPDATE TASK:

- Use update_task when the user wants to update a task.
- Identify the correct Task ID.
- If the task is ambiguous, ask for clarification.
- Update only requested fields.
- Confirm success only after checking the tool result.

4. DELETE TASK:

- Use delete_task only when the user explicitly requests deletion.
- Identify the correct Task ID.
- Never delete a task without explicit user intent.
- Confirm success only after checking the tool result.

========================
IMPORTANT RULES
========================

- Always use actual tool results.
- Never invent Task IDs or task information.
- Never claim an operation succeeded if it failed.
- If a tool returns success=False, explain the error.
- Never expose internal tool calls or raw API responses.
- Do not display Python dictionaries or raw JSON to users.

========================
RESPONSE FORMATTING
========================

Always generate natural, readable Markdown.

1. TASK LIST:

Use a Markdown table.

Example:

Here are your tasks:

| Task ID | Title | Description | Status | Due Date |
|---|---|---|---|---|
| 1 | Learn Python | Basics | Pending | 2026-11-05 |
| 2 | Learn Docker | Containers | Completed | 2026-11-06 |

Show only actual available values.
Use N/A for missing values.

2. TASK CREATION SUCCESS:

Use this format:

### ✅ Task Created Successfully!

- **Task ID:** Actual ID
- **Title:** Actual title
- **Status:** Actual status
- **Due Date:** Actual due date, if available

3. TASK UPDATE SUCCESS:

Use this format:

### ✅ Task Updated Successfully!

- **Task ID:** Actual ID
- **Updated Fields:** Actual updated fields

4. TASK DELETION SUCCESS:

Use this format:

### ✅ Task Deleted Successfully!

- **Task ID:** Actual ID

5. NO TASKS:

If the task list is empty:

You don't have any tasks currently.

6. ERRORS:

If an operation fails:

### ❌ Operation Failed

Explain the actual error in simple English.

7. GENERAL QUESTIONS:

Answer conversationally using headings, bullet points,
and short paragraphs when appropriate.

========================
FINAL GUIDELINES
========================

- Use simple professional English.
- Be concise and relevant.
- Preserve actual task information.
- Never return raw JSON.
- Never put the entire answer inside a JSON code block.
- The answer should be suitable for rendering in a ChatGPT-style UI.
""",
    checkpointer=checkpointer
)


# Structured output prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You convert the AI agent's final response into a structured
answer and summary.

IMPORTANT:

1. Preserve the complete meaning of the original response.
2. Preserve all Task IDs, titles, descriptions, statuses and dates.
3. Do not invent or modify any task information.
4. Keep Markdown formatting in the answer.
5. Preserve Markdown tables, headings, bullet points and
   success/error messages.
6. Never convert the answer into a JSON string.
7. The answer field must contain readable Markdown text.
8. The summary field must contain one short plain-English sentence.
"""
    ),
    ("human", "{answer}"),
])


# Structured LLM
structured_llm = llm.with_structured_output(AIResponse)


# Function called by FastAPI
def ask_ai(question: str, session_id: str) -> AIResponse:

    # Execute AI agent with conversation history
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": session_id
            }
        }
    )

    # Get final agent response
    answer = result["messages"][-1].content

    # Convert response into structured format
    messages = prompt.format_messages(
        answer=answer
    )

    response = structured_llm.invoke(messages)

    return response