from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from .schemas import CreateTask, DisplayTask, TaskStatus
from .utils import create_task, get_task, get_tasks, update_status, update_task

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=DisplayTask)
async def create_one_task(
    task_data: CreateTask, session: AsyncSession = Depends(get_session)
):
    new_task = await create_task(task_data, session)

    return new_task


@task_router.get("/", status_code=status.HTTP_200_OK, response_model=list[DisplayTask])
async def get_many_tasks(
    offset: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)
):
    tasks = await get_tasks(session, offset, limit)

    return tasks


@task_router.get("/{id}/", status_code=status.HTTP_200_OK, response_model=DisplayTask)
async def get_one_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await get_task(session, task_id)

    return task


@task_router.patch("/{id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_task_status(
    task_id: int, status: TaskStatus, session: AsyncSession = Depends(get_session)
):
    update = await update_status(session, task_id, status)

    return {"msg": "succesful"}


@task_router.patch(
    "/{id}/edit", status_code=status.HTTP_200_OK, response_model=DisplayTask
)
async def edit_task(
    task_id: int,
    task_data: CreateTask | None,
    session: AsyncSession = Depends(get_session),
):
    updated_task = await update_task(session, task_id, task_data)

    return updated_task
