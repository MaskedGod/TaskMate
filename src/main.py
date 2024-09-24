import asyncio
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import check_for_overdue_tasks
from .database import get_session

from .task.router import task_router
from .auth.router import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def periodic_task():
        async for session in get_session():
            while True:
                print("Overdue tasks check started")
                try:
                    print("Session acquired")
                    result = await check_for_overdue_tasks(session)
                    print("Overdue tasks check result:", result)
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    await asyncio.sleep(3600)  # Check every hour for testing

    task = asyncio.create_task(periodic_task())

    yield

    task.cancel()
    print("Task finished")


app = FastAPI(title="TaskMate", lifespan=lifespan)

app.include_router(task_router)
app.include_router(auth_router)


@app.get("/")
async def home():
    return {"msg": "it's on now!"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "Database connection is healthy!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}
