from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from queries.exercise_templates import (
    ExerciseTemplateIn,
    ExerciseTemplateOut,
    ExerciseTemplateRepo,
    UpdateExerciseTemplate,
    Error,
)

from typing import List, Union

router = APIRouter()

@router.post(
        "/api/exercise_templates",
        response_model=ExerciseTemplateOut,
        tags=["Exercise Templates"]
)
def create_exercise_templates(
    exercise_template: ExerciseTemplateIn,
    repo: ExerciseTemplateRepo = Depends(),
):
    return repo.create_exercise_template(
        exercise_template=exercise_template,
    )


@router.get(
    "/api/exercise_templates",
    response_model=Union[List[ExerciseTemplateOut], Error],
    tags=["Exercise Templates"]
)
def get_all_exercise_templates(
    repo: ExerciseTemplateRepo = Depends(),
):
    return repo.get_all_exercise_templates()


@router.get(
    "/api/exercise_templates/{exercise_template_id}",
    response_model=Union[ExerciseTemplateOut, Error],
    tags=["Exercise Templates"]
)
def get_one_exercise_template(
    exercise_template_id: int,
    repo: ExerciseTemplateRepo = Depends()
    ):
    exercise_template = repo.get_one_exercise_template(exercise_template_id)
    if exercise_template:
        return exercise_template
    else:
        raise HTTPException(status_code=404, detail="Exercise not found")

@router.put(
    "/api/exercise_templates/{exercise_template_id}",
    response_model=Union[ExerciseTemplateOut, Error],
    tags=["Exercise Templates"]
)
def update_one_exercise_template(
    exercise_template_id: int,
    exercise_template: UpdateExerciseTemplate,
    repo: ExerciseTemplateRepo = Depends(),
):
    result = repo.update_one_exercise_template(exercise_template_id, exercise_template)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="Exercise template not found or update failed"
        )


@router.delete(
    "/api/exercise_templates/{exercise_template_id}",
    response_model=dict,
    tags=["Exercise Templates"]
)
def delete_one_exercise_template(
    exercise_template_id: int,
    repo: ExerciseTemplateRepo = Depends(),
):
    return repo.delete_one_exercise_template(exercise_template_id)
