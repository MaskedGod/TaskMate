from datetime import date
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):

    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"
    # overdue = "overdue"


class CreateTask(BaseModel):

    title: str
    description: str
    status: TaskStatus
    # due_date: date | None


class DisplayTask(BaseModel):

    id: int
    title: str
    description: str
    status: TaskStatus
