from fastapi import FastAPI

from tasks import tasks


app = FastAPI(title="TaskMate")

app.include_router(tasks)


@app.get("/")
def home():
    return {"Chaos": "Reigns"}
