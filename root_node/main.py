from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


class CompletedJob(BaseModel):
    element1: str
    element2: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/job/", status_code=200)
async def get_next_job():
    return {"message": "Hello World"}


@app.post("/job/", status_code=200)
async def post_completed_job(job: CompletedJob):
    return {"message": "Hello World"}
