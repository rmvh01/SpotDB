from typing import Union
from routers.exercises_crud import exercise_records, exercise_templates, metric_templates, numeric_metric_records, string_metric_records
from fastapi import FastAPI

app = FastAPI()

app.include_router(exercise_templates.router)
app.include_router(exercise_records.router)
app.include_router(metric_templates.router)
app.include_router(numeric_metric_records.router)
app.include_router(string_metric_records.router)


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
