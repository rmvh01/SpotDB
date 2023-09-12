from pydantic import BaseModel
from queries.pool import pool


class Error(BaseModel):
    message: str


class ExerciseTemplateIn(BaseModel):
    name: str
    description: str
    type: str


class ExerciseTemplateOut(ExerciseTemplateIn):
    id: int
    name: str
    description: str
    type: str


class UpdateExerciseTemplate(ExerciseTemplateIn):
    name: str
    description: str
    type: str


class ExerciseTemplateRepo:
    # create one exercise template
    def create_exercise_template(self, exercise: ExerciseTemplateIn):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                result = cur.execute(
                    """
                    INSERT INTO exercise_templates
                        (name,
                        description,
                        type)
                    VALUES
                    (%s, %s, %s)
                    RETURNING id;
                    """,
                    [
                        exercise.name,
                        exercise.description,
                        exercise.type,
                    ],
                )
                id = result.fetchone()[0]
                data = exercise.dict()
                return ExerciseTemplateOut(id=id, **data)

    # get all exercise templates
    def get_all_exercise_templates(self):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, name, description, type
                        FROM exercise_templates
                        """,
                    )
                    result = cur.fetchall()
                    exercise = [
                        ExerciseTemplateOut(
                            id=row[0],
                            name=row[1],
                            description=row[2],
                            type=row[3],
                        )
                        for row in result
                    ]
                    return exercise
        except Exception:
            print({"message": "cannot get all exercise records"})
            return []

    # change an exercise template
    def update_one_exercise_template(
            self,
            exercise_template_id: int,
            exercise_template: UpdateExerciseTemplate
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE exercise_templates
                        SET
                            name = %s,
                            description = %s,
                            type = %s
                        WHERE id = %s;
                        """,
                        [
                            exercise_template.name,
                            exercise_template.description,
                            exercise_template_id
                        ],
                    )
                    if cur.rowcount:
                        return {"message": "exercise updated sucessfully!"}
                    else:
                        return None # more error handling here later
        except Exception:
            return {"message": "failed to update exercise"}
