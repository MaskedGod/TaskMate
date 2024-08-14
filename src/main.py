from typing import List
from fastapi import FastAPI


app = FastAPI(title="TaskMate")


@app.get("/")
def home():
    return {"Chaos": "Reigns"}
