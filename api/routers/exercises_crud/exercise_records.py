from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from queries.exercises.exercise_records import (
    UpdateExerciseRecord,
    ExerciseRecordIn,
    ExerciseRecordOut,
    ExerciseRecordRepo,
    Error
)

from typing import List, Union

router = APIRouter()

@router.post(
    "/api/exercise_records",
    response_model=ExerciseRecordOut,
    tags=["Exercise Records"]
)
def create_exercise_record(
    exercise_record: ExerciseRecordIn,
    repo: ExerciseRecordRepo = Depends(),
):
    return repo.create_exercise_record(
        exercise_record=exercise_record,
    )


@router.get(
    "/api/exercise_records",
    response_model=Union[List[ExerciseRecordOut], Error],
    tags=["Exercise Records"]
)
def get_all_exercise_records(
    repo: ExerciseRecordRepo = Depends(),
):
    return repo.get_all_exercise_records()


@router.get(
    "/api/exercise_records/{exercise_record_id}",
    response_model=Union[ExerciseRecordOut, Error],
    tags=["Exercise Records"]
)
def get_one_exercise_record(
    exercise_record_id: int,
    repo: ExerciseRecordRepo = Depends(),
):
    return repo.get_one_exercise_record(exercise_record_id=exercise_record_id)


@router.put(
    "/api/exercise_records/{exercise_record_id}",
    response_model=Union[ExerciseRecordOut, Error],
    tags=["Exercise Records"]
)
def update_one_exercise_record(
    exercise_record_id: int,
    exercise_record: UpdateExerciseRecord,
    repo: ExerciseRecordRepo = Depends(),
):
    result = repo.update_one_exercise_record(exercise_record_id, exercise_record)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="Exercise record not ofund or update failed"
        )


@router.delete(
    "/api/exercise_records/{exercise_record_id}",
    response_model=dict,
    tags=["Exercise Records"]
)
def delete_one_exercise_record(
    exercise_record_id: int,
    repo: ExerciseRecordRepo = Depends(),
):
    return repo.delete_one_exercise_record(exercise_record_id)
