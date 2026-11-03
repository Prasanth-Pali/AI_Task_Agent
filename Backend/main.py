
from datetime import datetime, timezone
from Backend.database import get_db
from Backend.models import Tasks
from Backend.llm import ask_ai
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


from fastapi.middleware.cors import CORSMiddleware

from Backend.schemas import ChatRequest, TaskCreate, TaskUpdate


app = FastAPI(
    title="AI Task Agent API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://ai-task-agent-frontend-0h60.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_task(task: Tasks) -> dict:
    """Convert a database model into the API response format."""
    return {
        "taskId": task.TaskId,
        "title": task.Title,
        "description": task.Description,
        "dueDateUtc": (
            task.DueDateUtc.isoformat()
            if task.DueDateUtc
            else None
        ),
        "status": task.Status,
        "createdAtUtc": (
            task.CreatedAtUtc.isoformat()
            if task.CreatedAtUtc
            else None
        ),
        "updatedAtUtc": (
            task.UpdatedAtUtc.isoformat()
            if task.UpdatedAtUtc
            else None
        ),
    }


def get_task_or_404(db: Session, task_id: int) -> Tasks:
    """Retrieve one task or raise 404 if it doesn't exist."""
    task = db.get(Tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} was not found.",
        )

    return task


# GET: Retrieve all tasks
@app.get("/api/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.scalars(
        select(Tasks).order_by(Tasks.TaskId)
    ).all()

    return [serialize_task(task) for task in tasks]


# POST: Create a task
@app.post("/api/tasks", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
):
    task = Tasks(
        Title=payload.title.strip(),
        Description=payload.description,
        DueDateUtc=payload.due_date_utc,
        Status=payload.status,
    )

    if not task.Title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task title cannot be empty.",
        )

    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        return serialize_task(task)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create task.",
        )

# PATCH: Update only the supplied fields
@app.patch("/api/tasks/{task_id}")
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update.",
        )

    if "title" in changes:
        if changes["title"] is None or not changes["title"].strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title cannot be empty.",
            )
        task.Title = changes["title"].strip()

    if "description" in changes:
        task.Description = changes["description"]

    if "due_date_utc" in changes:
        task.DueDateUtc = changes["due_date_utc"]

    if "status" in changes:
        if changes["status"] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Status cannot be null.",
            )
        task.Status = changes["status"]

    task.UpdatedAtUtc = datetime.now(timezone.utc).replace(tzinfo=None)

    try:
        db.commit()
        db.refresh(task)
        return serialize_task(task)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update task.",
        )


# DELETE: Delete a task
@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task_or_404(db, task_id)

    try:
        db.delete(task)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete task.",
        )

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = ask_ai(request.question,
                          request.session_id)

        return {
            "answer": response.answer,
            "summary": response.summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
