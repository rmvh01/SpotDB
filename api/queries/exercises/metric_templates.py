from pydantic import BaseModel
from queries.pool import pool

class MetricTemplateIn(BaseModel):
    name: str
    unit: str


class MetricTemplateOut(MetricTemplateIn):
    id: int
    name: str
    unit: str


class UpdateMetricTemplate(MetricTemplateIn):
    name: str
    unit: str


class Error(BaseModel):
    message: str

class MetricTemplatesRepo:

    def create_metric_template(self, metric_template: MetricTemplateIn):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                result = cur.execute(
                    """
                    INSERT INTO metric_templates
                        (name,
                        unit)
                    VALUES
                    (%s, %s)
                    RETURNING id;
                    """,
                    [
                        metric_template.name,
                        metric_template.unit
                    ],
                )
                id = result.fetchone()[0]
                data = metric_template.model_dump()
                return MetricTemplateOut(id=id, **data)

    def get_all_metric_templates(self):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, name, unit
                        FROM metric_templates
                        """,
                    )
                    result = cur.fetchall()
                    metric_template = [
                        MetricTemplateOut(
                        id=row[0],
                        name=row[1],
                        unit=row[2],
                        )
                        for row in result
                    ]
                    return metric_template
        except Exception:
            print({"message": "cannot get all metric templates"})
            return []

    def get_one_metric_template(
        self,
        metric_template_id: int,
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, name, unit
                        FROM metric_templates
                        WHERE id = %s;
                        """,
                        [metric_template_id]
                    )
                    row = cur.fetchone()
                    if row:
                        return MetricTemplateOut(
                            id=row[0],
                            name=row[1],
                            unit=row[2],
                        )
                    else:
                        return None
        except Exception:
            return {"Message": "Failed to fetch metric template"}


    def update_one_metric_template(
        self,
        metric_template_id: int,
        metric_template: UpdateMetricTemplate
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE metric_templates
                        SET
                            name = %s,
                            unit = %s
                        WHERE id = %s;
                        """,
                        [
                            metric_template.name,
                            metric_template.unit,
                            metric_template_id
                        ],
                    )
                    if cur.rowcount:
                        return {"message": "metric template updated successfully!"}
                    else:
                        return None
        except Exception as e:
            return {"message": "failed to update metric template", "error": e}

    def delete_one_metric_template(
        self,
        metric_template_id: int,
    ):
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM metric_templates
                        WHERE id = %s;
                        """,
                        [metric_template_id]
                    )
                    return {"message": "Metric template deleted successfully!"}
        except Exception:
            return {"message": "Failed to delete metric template."}
