
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TaskStatus = Literal["Pending", "InProgress", "Completed"]


class TaskCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    due_date_utc: datetime | None = Field(
        default=None,
        alias="dueDateUtc",
    )
    status: TaskStatus = "Pending"


class TaskUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    due_date_utc: datetime | None = Field(
        default=None,
        alias="dueDateUtc",
    )
    status: TaskStatus | None = None

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    session_id: str



