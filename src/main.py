from fastapi import FastAPI

from .routers import users


app = FastAPI(title="TaskMate")

app.include_router(users.router)


@app.get("/")
def home():
    return {"Chaos": "Reigns"}
