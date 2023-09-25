from pydantic import BaseModel
from queries.pool import pool
from datetime import date, time


class Error(BaseModel):
    message: str


class ExerciseRecordIn(BaseModel):
    exercise_template_id: int
    date: date
    time: time


class ExerciseRecordOut(ExerciseRecordIn):
    id: int
    exercise_template_id: int
    date: date
    time: time


class UpdateExerciseRecord(ExerciseRecordIn):
    exercise_template_id: int
    date: date
    time: time


class ExerciseRecordRepo:
    def create_exercise_record(self, exercise_record: ExerciseRecordIn):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                result = cur.execute(
                    """
                    INSERT INTO exercise_records
                        (exercise_template_id,
                        date,
                        time)
                    VALUES
                    (%s, %s, %s)
                    RETURNING id;
                    """,
                    [
                        exercise_record.exercise_template_id,
                        exercise_record.date,
                        exercise_record.time,
                    ]
                )
                id = result.fetchone()[0]
                data = exercise_record.model_dump()
                return ExerciseRecordOut(id=id, **data)

    def get_all_exercise_records(self):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, exercise_template_id, date, time
                        FROM exercise_records
                        """,
                    )
                    result = cur.fetchall()
                    exercise_records = [
                        ExerciseRecordOut(
                            id=row[0],
                            exercise_template_id=row[1],
                            date=row[2],
                            time=row[3],
                        )
                        for row in result
                    ]
                    return exercise_records
        except Exception:
            print({"message": "cannot get all exercise records"})
            return []

    def get_one_exercise_record(self, exercise_record_id: int):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, exercise_template_id, date, time
                        FROM exercise_records
                        WHERE id = %s;
                        """,
                        [exercise_record_id]
                    )
                    row = cur.fetchone()
                    if row:
                        return ExerciseRecordOut(
                            id=row[0],
                            exercise_template_id=row[1],
                            date=row[2],
                            time=row[3]
                        )
                    else:
                        return None
        except Exception:
            return {"Message": "Failed to fetch that exercise record"}



    def update_one_exercise_record(
        self,
        exercise_record_id: int,
        exercise_record: UpdateExerciseRecord
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE exercise_records
                        SET
                            exercise_template_id = %s,
                            date = %s,
                            time = %s
                        WHERE id = %s;
                        """,
                        [
                            exercise_record.exercise_template_id,
                            exercise_record.date,
                            exercise_record.time,
                            exercise_record_id
                        ],
                    )
                    if cur.rowcount:
                        return {"message": "exercise updated successfully!"}
                    else:
                        return None # more error handling later
        except Exception as e:
            return {"message": "failed to update exericse", "error": e}


    def delete_one_exercise_record(
        self,
        exercise_record_id: int,
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM exercise_records
                        WHERE id = %s;
                        """,
                        [exercise_record_id],
                    )
                    return {"message": "Exercise record deleted successfully!"}
        except Exception:
            return {"message": "Failed to delete exercise record."}
