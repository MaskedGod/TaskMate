from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .task.models import Task


async def check_for_overdue_tasks(session: AsyncSession):
    stmt = select(Task).filter(
        Task.due_date < datetime.now(timezone.utc).date(), Task.status != "overdue"
    )
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    for task in tasks:
        task.status = "overdue"
        task.updated_at = datetime.now()
    await session.commit()

    return f"{len(tasks)} Changed"
