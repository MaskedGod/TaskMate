from datetime import date
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):

    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class TaskStatusInsider(str, Enum):

    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"
    overdue = "overdue"


class CreateTask(BaseModel):

    title: str
    description: str
    status: TaskStatus
    due_date: date | None


class EditTask(BaseModel):

    title: str
    description: str
    status: TaskStatus


class DisplayTask(BaseModel):

    id: int
    title: str
    description: str
    status: TaskStatusInsider
    due_date: date
