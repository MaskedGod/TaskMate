from datetime import date, datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Task
from .schemas import CreateTask, EditTask


async def find_task_by_id(session: AsyncSession, task_id: int, current_user):

    stmt = select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


async def create_one_task(
    session: AsyncSession, task_data: CreateTask, current_user
) -> Task:
    try:
        new_task = Task(owner_id=current_user.id, **task_data.model_dump())
        if not new_task.title or not new_task.description or not new_task.status:
            raise ValueError("All fields must be provided and cannot be empty.")

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


async def get_many_tasks(session: AsyncSession, offset: int, limit: int, current_user):
    stmt = select(Task).filter(Task.owner_id == current_user.id)
    result = await session.execute(stmt)
    tasks = result.scalars().all()

    return tasks[offset : offset + limit]


async def update_task(
    session: AsyncSession, task_id: int, task_data: EditTask, current_user
):
    task = await find_task_by_id(session, task_id, current_user)

    if len(task_data.title) > 0:
        task.title = task_data.title
    if len(task_data.title) > 0:
        task.description = task_data.description
    if len(task_data.title) > 0:
        task.status = task_data.status

    task.updated_at = datetime.now()

    await session.commit()
    await session.refresh(task)

    return task


async def update_status(session: AsyncSession, task_id: int, status: str, current_user):
    task = await find_task_by_id(session, task_id, current_user)

    task.status = status
    task.updated_at = datetime.now()

    await session.commit()

    return "status updated"


async def remove_task(session: AsyncSession, task_id: int, current_user):
    task = await find_task_by_id(session, task_id, current_user)

    await session.delete(task)
    await session.commit()

    return {"msg": "deleted"}


async def update_due_date(
    session: AsyncSession, task_id: int, new_due_date: date, current_user
):
    task = await find_task_by_id(session, task_id, current_user)

    if new_due_date < datetime.now(timezone.utc).date():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The new due date cannot be in the past",
        )

    task.due_date = new_due_date
    task.updated_at = datetime.now()

    await session.commit()

    return "Due data updated"
