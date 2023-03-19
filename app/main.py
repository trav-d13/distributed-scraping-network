from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List


class CompletedJob(BaseModel):
    id: int
    lat: float
    long: float
    observed_on: str  # Date and time of observation
    time_zone: str
    elevation: float
    time: str  # Time from which daily variables were extracted

    # Daily variables
    temperature_2m: float
    relativehumidity_2m: float
    dewpoint_2m: float
    apparent_temperature: float
    surface_pressure: float
    precipitation: float
    rain: float
    snowfall: float
    cloudcover: float
    cloudcover_low: float
    cloudcover_mid: float
    cloudcover_high: float
    shortwave_radiation: float
    direct_radiation: float
    diffuse_radiation: float
    windspeed_10m: float
    windspeed_100m: float
    winddirection_10m: float
    winddirection_100m: float
    windgusts_10m: float
    et0_fao_evapotranspiration_hourly: float
    weathercode_hourly: int
    vapor_pressure_deficit: float
    soil_temperature_0_to_7cm: float
    soil_temperature_7_to_28cm: float
    soil_temperature_28_to_100cm: float
    soil_moisture_0_to_7cm: float
    soil_moisture_7_to_28cm: float
    soil_moisture_28_to_100cm: float

    # Daily variables
    weathercode_daily: int
    temperature_2m_max: float
    temperature_2m_min: float
    apparent_temperature_max: float
    apparent_temperature_min: float
    precipitation_sum: float
    rain_sum: float
    snowfall_sum: float
    precipitation_hours: float
    sunrise: str
    sunset: str
    windspeed_10m_max: float
    windgusts_10m_max: float
    winddirection_10m_dominant: float
    shortwave_radiation_sum: float
    et0_fao_evapotranspiration_daily: float

class JobInfo(BaseModel):
    id: int
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    obs_time: str


def format_job_info(response: str) -> JobInfo:
    response = response.strip().split(",")
    return JobInfo(id=int(response[0]), latitude=float(response[3]), longitude=float(response[4]),
                   start_date=response[1], end_date=response[1], obs_time=response[2])


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
    vars["index"] = vars["index"] + 1
    return format_job_info(response)


@app.post("/job/", status_code=200)
async def post_completed_job(job: CompletedJob):
    with open("completed_data.csv", "a") as file:
        file.write(str(job))


@app.get("/jobs_completed/", status_code=200)
async def get_all_completed_jobs(start: int | None, end: int | None):
    with open("completed_data.csv", "r") as file:
        data = file.readlines()
    return data
