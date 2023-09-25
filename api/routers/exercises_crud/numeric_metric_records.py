from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from queries.exercises.numeric_metric_records import (
    NumericMetricRecordIn,
    NumericMetricRecordOut,
    UpdateNumericMetricRecord,
    NumericMetricRecordsRepo,
    Error
)

from typing import List, Union

router = APIRouter()

@router.post(
    "/api/exercise_records/{exercise_record_id}/numeric_metric_records",
    response_model=Union[NumericMetricRecordOut, Error],
    tags=["Numeric Metric Records"]
)
def create_numeric_metric_record(
    metric_record: NumericMetricRecordIn,
    exercise_record_id: int,
    repo: NumericMetricRecordsRepo = Depends(),
):
    return repo.create_numeric_metric_record(
        metric_record=metric_record,
        exercise_record_id=exercise_record_id
    )

@router.get(
    "/api/exercise_records/{exercise_record_id}/numeric_metric_records",
    response_model=Union[List[NumericMetricRecordOut], Error],
    tags=["Numeric Metric Records"]
)
def get_numeric_metric_records(
    exercise_record_id: int,
    repo: NumericMetricRecordsRepo = Depends(),
):
    return repo.get_numeric_metric_records(
        exercise_record_id=exercise_record_id
    )

@router.put(
    "/api/exercise_records/{exercise_record_id}/numeric_metric_records/{numeric_metric_record_id}",
    response_model=Union[dict, Error],
    tags=["Numeric Metric Records"]
)
def update_numeric_metric_record(
    exercise_record_id: int,
    numeric_metric_record_id: int,
    numeric_metric_record: UpdateNumericMetricRecord,
    repo: NumericMetricRecordsRepo = Depends(),
):
    return repo.update_numeric_metric_record(
        exercise_record_id=exercise_record_id,
        numeric_metric_record_id=numeric_metric_record_id,
        numeric_metric_record=numeric_metric_record
    )

@router.delete(
    "/api/exercise_records/{exercise_record_id}/numeric_metric_records/{numeric_metric_record_id}",
    response_model=dict,
    tags=["Numeric Metric Records"]
)
def delete_numeric_metric_record(
    numeric_metric_record_id: int,
    repo: NumericMetricRecordsRepo = Depends(),
):
    return repo.delete_numeric_metric_record(
        numeric_metric_record_id=numeric_metric_record_id
    )
