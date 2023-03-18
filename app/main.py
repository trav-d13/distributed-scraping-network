from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List


class CompletedJob(BaseModel):
    id: int
    lat: float
    lon: float
    observed_on: str
    generationtime_ms: float
    timezone: str
    elevation: float
    time: List[str]
    temperature_2m: List[float]
    dewpoint_2m: List[float]

class JobInfo(BaseModel):
    id: int
    latitude: float
    longitude: float
    start_date: str
    end_date: str


vars = {}

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    vars["index"] = 0
    with open("interim_sample.csv", "r") as file:
        data = file.readlines()

    vars["data"] = data


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/job/", status_code=200)
async def get_next_job():
    data = vars["data"]
    index = vars["index"]
    response = data[index]
    response = response.strip().split(",")
    vars["index"] = vars["index"] + 1
    return JobInfo(id = int(response[0]), latitude = float(response[3]), longitude = float(response[4]),
                    start_date = response[1], end_date = response[1])


@app.post("/job/", status_code=200)
async def post_completed_job(job: CompletedJob):
    with open("completed_data.csv", "a") as file:
        file.write(str(job))


@app.get("/jobs_completed/", status_code=200)
async def get_all_completed_jobs(start: int | None, end: int | None):
    with open("completed_data.csv", "r") as file:
        data = file.readlines()
    return data
