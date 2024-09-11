from fastapi import Depends, FastAPI, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from contextlib import asynccontextmanager

from .database import get_session

from .task.router import task_router
from .auth.router import auth_router


app = FastAPI(title="TaskMate")

app.include_router(task_router)
app.include_router(auth_router)

# scheduler = AsyncIOScheduler()


# async def check_task_expiry():
#     # logic for checking and updating expired tasks
#     print("Checking for expired tasks...")


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     scheduler.add_job(check_task_expiry, "interval", minutes=60)
#     scheduler.start()
#     print("Scheduler started")
#     yield
#     print("Shutting down scheduler")
#     scheduler.shutdown()


# app.router.lifespan_context = lifespan


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "Database connection is healthy!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}
