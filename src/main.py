from fastapi import FastAPI

from .task.router import task_router


app = FastAPI(title="TaskMate")

app.include_router(task_router)


@app.get("/")
def home():
    return {"Chaos": "Reigns"}
