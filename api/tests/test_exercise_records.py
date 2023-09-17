from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from queries.exercise_records import (
    ExerciseRecordIn,
    ExerciseRecordOut,
    ExerciseRecordRepo,
    UpdateExerciseRecord
)

client = TestClient(app)


valid_date = str(datetime.now().date())
valid_time = str(datetime.now().time())

class FakeExerciseRecordRepo:

    def create_exercise_record(self, exercise_record):
        return ExerciseRecordOut(
            id=999,
            exercise_id=exercise_record.exercise_id,
            date=exercise_record.date,
            time=exercise_record.time,
        )

    def get_all_exercise_records(self):
        return [
        {
            "id": 1,
            "exercise_id": 1,
            "date": valid_date,
            "time": valid_time,
        },
        {
            "id": 2,
            "exercise_id": 1,
            "date": valid_date,
            "time": valid_time,
        },
    ]

    def get_one_exercise_record(self, exercise_record_id: int):
        return {
        "id": exercise_record_id,
        "exercise_id": 1,
        "date": valid_date,
        "time": valid_time,
        }

    def update_one_exercise_record(
            self,
            exercise_record_id: int,
            exercise_record: UpdateExerciseRecord
            ):
        return {
            "id": exercise_record_id,
            "exercise_id": exercise_record.exercise_id,
            "date": exercise_record.date,
            "time": exercise_record.time,
        }

    def delete_one_exercise_record(
            self,
            exercise_record_id: int
    ):
        if exercise_record_id == 1:
            return {"message": "Exercise record deleted successfully!"}
        else:
            return {"message": "Failed to delete exercise record."}


def test_create_exercise_record():
    app.dependency_overrides[ExerciseRecordRepo] = FakeExerciseRecordRepo


    new_exercise_record = {
        "exercise_id": 999,
        "date": valid_date,
        "time": valid_time,
    }
    print(new_exercise_record)

    response = client.post("/api/exercise_records", json=new_exercise_record)
    data = response.json()

    assert response.status_code == 200
    assert data["exercise_id"] == new_exercise_record["exercise_id"]
    assert data["date"] == new_exercise_record["date"]
    assert data["time"] == new_exercise_record["time"]

def test_get_all_exercise_records():
    app.dependency_overrides[ExerciseRecordRepo] = FakeExerciseRecordRepo

    response = client.get("/api/exercise_records")
    data = response.json()

    assert response.status_code == 200
    assert data == [
        {
            "id": 1,
            "exercise_id": 1,
            "date": valid_date,
            "time": valid_time,
        },
        {
            "id": 2,
            "exercise_id": 1,
            "date": valid_date,
            "time": valid_time,
        },
    ]

def test_get_one_exercise_record():
    app.dependency_overrides[ExerciseRecordRepo] = FakeExerciseRecordRepo

    response = client.get("/api/exercise_records/1")
    data = response.json()

    expected = {
        "id": 1,
        "exercise_id": 1,
        "date": valid_date,
        "time": valid_time,
    }

    assert response.status_code == 200
    assert data == expected

def test_update_one_exercise_record():
    app.dependency_overrides[ExerciseRecordRepo] = FakeExerciseRecordRepo

    new_record = {
        "id": 1,
        "exercise_id": 2,
        "date": valid_date,
        "time": valid_time,
    }
    response = client.put("/api/exercise_records/1", json=new_record)
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["id"] == new_record["id"]
    assert data["exercise_id"] == new_record["exercise_id"]
    assert data["date"] == new_record["date"]
    assert data["time"] == new_record["time"]

def test_delete_one_exercise_record():
    app.dependency_overrides[ExerciseRecordRepo] = FakeExerciseRecordRepo
    response = client.delete("/api/exercise_records/1")
    data = response.json()

    assert response.status_code == 200
    assert data == {"message": "Exercise record deleted successfully!"}

    response_fail = client.delete("/api/exercise_records/2")
    data_fail = response_fail.json()

    assert response_fail.status_code == 200
    assert data_fail == {"message": "Failed to delete exercise record."}
