from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Task
from .schemas import CreateTask


async def create_task(
    session: AsyncSession, task_data: CreateTask, current_user
) -> Task:

    new_task = Task(**task_data.model_dump())

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


async def get_tasks(session: AsyncSession, offset: int, limit: int):

    result = await session.execute(select(Task).offset(offset).limit(limit))
    tasks = result.scalars().all()

    return tasks


async def get_task(session: AsyncSession, task_id: int):

    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


async def update_status(session: AsyncSession, task_id: int, status: str):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status

    task.updated_at = datetime.now()

    await session.commit()

    return


async def update_task(session: AsyncSession, task_id: int, task_data: CreateTask):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status

    task.updated_at = datetime.now()

    await session.commit()
    await session.refresh(task)

    return task
