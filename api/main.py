from typing import Union
from fastapi import FastAPI
from routers import exercise_templates, exercise_records

app = FastAPI()

app.include_router(exercise_templates.router)
app.include_router(exercise_records.router)


@app.get("/api/launch-details")
def launch_details():
    return {
        "launch_details": {
            "module": 3,
            "week": 17,
            "day": 5,
            "hour": 19,
            "min": "00"
        }
    }
