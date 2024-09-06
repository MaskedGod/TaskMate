from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.utils import get_current_user
from ..database import get_session
from .schemas import CreateTask, DisplayTask, TaskStatus
from .utils import (
    create_one_task,
    find_task_by_id,
    get_many_tasks,
    remove_task,
    update_status,
    update_task,
)

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=DisplayTask)
async def create_task(
    task_data: CreateTask,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):

    new_task = await create_one_task(session, task_data, current_user)

    return new_task


@task_router.get("/", status_code=status.HTTP_200_OK, response_model=list[DisplayTask])
async def get_tasks(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    tasks = await get_many_tasks(session, offset, limit, current_user)

    return tasks


@task_router.get("/id", status_code=status.HTTP_200_OK, response_model=DisplayTask)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    task = await find_task_by_id(session, task_id, current_user)

    return task


@task_router.patch("/id/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_task_status(
    task_id: int,
    status: TaskStatus,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    update = await update_status(session, task_id, status, current_user)

    return {"msg": update}


@task_router.patch(
    "/id/edit", status_code=status.HTTP_200_OK, response_model=DisplayTask
)
async def edit_task(
    task_id: int,
    task_data: CreateTask | None,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    updated_task = await update_task(session, task_id, task_data, current_user)

    return updated_task


@task_router.delete("/id/delete", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await remove_task(session, task_id, current_user)

    return result
