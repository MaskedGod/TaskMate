from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):

    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class CreateTask(BaseModel):

    title: str
    description: str
    status: TaskStatus


class DisplayTask(BaseModel):

    id: int
    title: str
    description: str
    status: TaskStatus
