from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from queries.exercises.string_metric_records import (
    StringMetricRecordsRepo,
    StringMetricRecordIn,
    StringMetricRecordOut,
    UpdateStringMetricRecord,
    Error
)

from typing import List, Union

router = APIRouter()

@router.post(
    "/api/exercise_records/{exercise_record_id}/string_metric_records",
    response_model=Union[StringMetricRecordOut, Error],
    tags=["String Metric Records"]
)
def create_numeric_metric_record(
    metric_record: StringMetricRecordIn,
    exercise_record_id: int,
    repo: StringMetricRecordsRepo = Depends(),
):
    return repo.create_string_metric_record(
        metric_record=metric_record,
        exercise_record_id=exercise_record_id
    )

@router.get(
    "/api/exercise_records/{exercise_record_id}/string_metric_records",
    response_model=Union[List[StringMetricRecordOut], Error],
    tags=["String Metric Records"]
)
def get_string_metric_records(
    exercise_record_id: int,
    repo: StringMetricRecordsRepo = Depends(),
):
    return repo.get_string_metric_records(
        exercise_record_id=exercise_record_id
    )

@router.put(
    "/api/exercise_records/{exercise_record_id}/string_metric_records/{string_metric_record_id}",
    response_model=Union[dict, Error],
    tags=["String Metric Records"]
)
def update_string_metric_record(
    exercise_record_id: int,
    string_metric_record_id: int,
    string_metric_record: UpdateStringMetricRecord,
    repo: StringMetricRecordsRepo = Depends(),
):
    return repo.update_string_metric_record(
        exercise_record_id=exercise_record_id,
        string_metric_record_id=string_metric_record_id,
        string_metric_record=string_metric_record
    )

@router.delete(
    "/api/exercise_records/{exercise_record_id}/string_metric_records/{string_metric_record_id}",
    response_model=dict,
    tags=["String Metric Records"]
)
def delete_string_metric_record(
    string_metric_record_id: int,
    repo: StringMetricRecordsRepo = Depends(),
):
    return repo.delete_string_metric_record(
        string_metric_record_id=string_metric_record_id
    )
