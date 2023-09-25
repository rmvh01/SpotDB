from fastapi.testclient import TestClient
from main import app
from queries.exercises.numeric_metric_records import (
    NumericMetricRecordIn,
    NumericMetricRecordOut,
    UpdateNumericMetricRecord,
    NumericMetricRecordsRepo,
)

client = TestClient(app)

class FakeNumericMetricRecordRepo:

    def create_numeric_metric_record(
        self,
        exercise_record_id: int,
        metric_record: NumericMetricRecordIn,
    ):
        return NumericMetricRecordOut(
            id=1,
            value=metric_record.value,
            metric_template_id=metric_record.metric_template_id,
            exercise_record_id=exercise_record_id,
        )

    def get_numeric_metric_records(self, exercise_record_id: int):
        return [
            {
                "id": 1,
                "value": 10,
                "metric_template_id": 1,
                "exercise_record_id": exercise_record_id,
            },
            {
                "id": 2,
                "value": 10,
                "metric_template_id": 2,
                "exercise_record_id": exercise_record_id,
            }
        ]

    def update_numeric_metric_record(
        self,
        exercise_record_id: int,
        numeric_metric_record_id: int,
        numeric_metric_record: UpdateNumericMetricRecord,
    ):
        return {
            "id": numeric_metric_record_id,
            "value": numeric_metric_record.value,
            "metric_template_id": numeric_metric_record.metric_template_id,
            "exercise_record_id": exercise_record_id
        }

    def delete_numeric_metric_record(
        self,
        numeric_metric_record_id: int,
    ):
        if numeric_metric_record_id == 1:
            return {"message": "Numeric metric record deleted successfully!"}
        else:
            return {"message": "Failed to delete numeric metric record."}


def test_create_numeric_metric_record():
    app.dependency_overrides[NumericMetricRecordsRepo] = FakeNumericMetricRecordRepo

    new_numeric_metric_record = {
        "value": 10,
        "metric_template_id": 1,
        "exercise_record_id": 1,
    }

    response = client.post("/api/exercise_records/1/numeric_metric_records", json=new_numeric_metric_record)
    data = response.json()

    assert response.status_code == 200
    assert data["value"] == new_numeric_metric_record["value"]
    assert data["metric_template_id"] == new_numeric_metric_record["metric_template_id"]
    assert data["exercise_record_id"] == new_numeric_metric_record["exercise_record_id"]

def test_get_numeric_metric_records():
    app.dependency_overrides[NumericMetricRecordsRepo] = FakeNumericMetricRecordRepo
    response = client.get("/api/exercise_records/1/numeric_metric_records")
    data = response.json()
    expected = [
        {
            "id": 1,
            "value": 10,
            "metric_template_id": 1,
            "exercise_record_id": 1,
        },
        {
            "id": 2,
            "value": 10,
            "metric_template_id": 2,
            "exercise_record_id": 1,
        },
    ]

    assert response.status_code == 200
    assert data == expected

def test_update_numeric_metric_record():
    app.dependency_overrides[NumericMetricRecordsRepo] = FakeNumericMetricRecordRepo

    new_record = {
        "id": 1,
        "value": 20,
        "metric_template_id": 1,
        "exercise_record_id": 1,
    }

    response = client.put(
        "/api/exercise_records/1/numeric_metric_records/1",
        json=new_record,
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == new_record["id"]
    assert data["value"] == new_record["value"]
    assert data["metric_template_id"] == new_record["metric_template_id"]
    assert data["exercise_record_id"] == new_record["exercise_record_id"]

def test_delete_numeric_metric_record():
    app.dependency_overrides[NumericMetricRecordsRepo] = FakeNumericMetricRecordRepo
    response = client.delete("/api/exercise_records/1/numeric_metric_records/1")
    data = response.json()

    assert response.status_code == 200
    assert data == {"message": "Numeric metric record deleted successfully!"}

    response_fail = client.delete("/api/exercise_records/1/numeric_metric_records/2")
    data_fail = response_fail.json()

    assert response_fail.status_code == 200
    assert data_fail == {"message": "Failed to delete numeric metric record."}
