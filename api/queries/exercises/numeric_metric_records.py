from fastapi import HTTPException
from pydantic import BaseModel
from queries.pool import pool

class NumericMetricRecordIn(BaseModel):
    value: int
    metric_template_id: int


class NumericMetricRecordOut(NumericMetricRecordIn):
    id: int
    value: int
    metric_template_id: int
    exercise_record_id: int


class UpdateNumericMetricRecord(NumericMetricRecordIn):
    value: int
    metric_template_id: int


class Error(BaseModel):
    message: str


class NumericMetricRecordsRepo:

    def create_numeric_metric_record(
        self,
        metric_record: NumericMetricRecordIn,
        exercise_record_id: int,
    ):
        print(metric_record, exercise_record_id)
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    result = cur.execute(
                        """
                        INSERT INTO numeric_metric_records
                            (value,
                            metric_template_id,
                            exercise_record_id)
                        VALUES
                        (%s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            metric_record.value,
                            metric_record.metric_template_id,
                            exercise_record_id,
                        ],
                    )
                    id = result.fetchone()[0]
                    data = metric_record.model_dump()
                    return NumericMetricRecordOut(id=id, exercise_record_id=exercise_record_id, **data)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error.")

    def get_numeric_metric_records(
            self,
            exercise_record_id: int,
        ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id,
                            value,
                            metric_template_id,
                            exercise_record_id
                        FROM numeric_metric_records
                        WHERE exercise_record_id = %s;
                        """,
                        [exercise_record_id]
                    )
                    result = cur.fetchall()
                    numeric_metric_records = [
                        NumericMetricRecordOut(
                            id=row[0],
                            value=row[1],
                            metric_template_id=row[2],
                            exercise_record_id=row[3],
                        )
                        for row in result
                    ]
                    return numeric_metric_records
        except Exception as e:
            print("error")
            return []

    def update_numeric_metric_record(
        self,
        exercise_record_id: int,
        numeric_metric_record_id: int,
        numeric_metric_record: UpdateNumericMetricRecord
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE numeric_metric_records
                        SET
                            value = %s,
                            metric_template_id = %s,
                            exercise_record_id = %s
                        WHERE id = %s;
                        """,
                        [
                            numeric_metric_record.value,
                            numeric_metric_record.metric_template_id,
                            exercise_record_id,
                            numeric_metric_record_id
                        ],
                    )
                    if cur.rowcount:
                        return {"message": "record updated successfully"}
                    else:
                        return {"message": "record failed to update"}
        except:
            print("error")


    def delete_numeric_metric_record(
        self,
        numeric_metric_record_id: int,
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM numeric_metric_records
                        WHERE id = %s;
                        """,
                        [numeric_metric_record_id]
                    )
                    return {"message": "exercise record deleted"}
        except:
            print("error")
