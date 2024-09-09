from fastapi import Depends, FastAPI, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session

from .task.router import task_router
from .auth.router import auth_router


app = FastAPI(title="TaskMate")

app.include_router(task_router)
app.include_router(auth_router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "Database connection is healthy!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}
