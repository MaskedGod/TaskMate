from fastapi import APIRouter, Depends, Query, status
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

MAX_LIMIT = 100


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
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=MAX_LIMIT, ge=0),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    tasks = await get_many_tasks(session, offset, limit, current_user)

    return tasks


@task_router.get("/id", status_code=status.HTTP_200_OK, response_model=DisplayTask)
async def get_task_by_id(
    task_id: int = Query(default=1, ge=1),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    task = await find_task_by_id(session, task_id, current_user)

    return task


@task_router.patch("/id/status", status_code=status.HTTP_200_OK)
async def update_task_status(
    status: TaskStatus | None,
    task_id: int = Query(default=1, ge=1),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    update = await update_status(session, task_id, status, current_user)

    return {"msg": update}


@task_router.patch(
    "/id/edit", status_code=status.HTTP_200_OK, response_model=DisplayTask
)
async def edit_task(
    task_data: CreateTask | None,
    task_id: int = Query(default=1, ge=1),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    updated_task = await update_task(session, task_id, task_data, current_user)

    return updated_task


@task_router.delete("/id/delete", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: int = Query(default=1, ge=1),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await remove_task(session, task_id, current_user)

    return result
