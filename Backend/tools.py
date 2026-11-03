
from typing import Literal

import requests
from langchain.tools import tool

import os

API_BASE_URL = os.getenv(
    "TASK_API_BASE_URL",
    f"http://127.0.0.1:{os.getenv('PORT', '8000')}"
).rstrip("/")

TaskStatus = Literal["Pending", "InProgress", "Completed"]


# Common API function
def call_api(method: str, endpoint: str, **kwargs):

    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            timeout=15,
            **kwargs,
        )

        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return {
                "success": True,
                "message": "Operation completed successfully."
            }

        result = response.json()

        # Preserve API response data
        return result

    except requests.HTTPError as exc:

        status_code = (
            exc.response.status_code
            if exc.response is not None else "unknown"
        )

        detail = (
            exc.response.text
            if exc.response is not None else str(exc)
        )

        return {
            "success": False,
            "statusCode": status_code,
            "error": detail,
        }

    except requests.RequestException as exc:

        return {
            "success": False,
            "error": f"Unable to connect to the Task API: {exc}",
        }


# Get all tasks
@tool
def get_all_tasks() -> dict | list:
    """Get all tasks from the database.

    MUST be used whenever the user asks to show, list,
    view, or retrieve all tasks.
    Returns actual task records from the Task API.
    """
    return call_api("GET", "/api/tasks")


# Create task
@tool
def create_task(
    title: str,
    description: str | None = None,
    due_date_utc: str | None = None,
    status: TaskStatus = "Pending",
) -> dict:
    """Create a new task in the database.

    Requires a task title.
    Optional fields are description, due date, and status.
    Valid statuses: Pending, InProgress, Completed.
    """
    payload = {
        "title": title,
        "description": description,
        "dueDateUtc": due_date_utc,
        "status": status,
    }

    return call_api("POST", "/api/tasks", json=payload)


# Update task
@tool
def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    due_date_utc: str | None = None,
    status: TaskStatus | None = None,
) -> dict:
    """Partially update an existing task.

    Requires the correct Task ID.
    Only update the fields requested by the user.
    Valid statuses: Pending, InProgress, Completed.
    """

    payload = {}

    if title is not None:
        payload["title"] = title

    if description is not None:
        payload["description"] = description

    if due_date_utc is not None:
        payload["dueDateUtc"] = due_date_utc

    if status is not None:
        payload["status"] = status

    if not payload:
        return {
            "success": False,
            "error": "Provide at least one field to update."
        }

    return call_api(
        "PATCH",
        f"/api/tasks/{task_id}",
        json=payload
    )


# Delete task
@tool
def delete_task(task_id: int) -> dict:
    """Permanently delete a task using its Task ID.

    Use only when the user explicitly requests deletion.
    """

    result = call_api("DELETE", f"/api/tasks/{task_id}")

    if isinstance(result, dict) and result.get("success") is True:
        return {
            "success": True,
            "message": f"Task {task_id} was deleted successfully."
        }

    return result


# AI Chat API tool
@tool
def ask_task_assistant(question: str) -> dict:
    """Send a question to the AI Task Assistant API.
    Returns an AI-generated answer and summary.
    Do not use this tool from inside the same AI agent.
    """

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={"question": question},
            timeout=60,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as exc:

        return {
            "success": False,
            "error": f"Unable to connect to AI Chat API: {exc}"
        }
