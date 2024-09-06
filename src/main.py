from fastapi import FastAPI

from .task.router import task_router
from .auth.router import auth_router


app = FastAPI(title="TaskMate")

app.include_router(task_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"msg": "Chaos Reigns"}
