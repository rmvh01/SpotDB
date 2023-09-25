from fastapi.testclient import TestClient
from main import app
from queries.exercises.exercise_templates import (
    ExerciseTemplateRepo,
    ExerciseTemplateOut,
    UpdateExerciseTemplate
)

client = TestClient(app)


class FakeExerciseTemplateRepo:

    def create_exercise_template(self, exercise_template):
        return ExerciseTemplateOut(
            id=999,
            name=exercise_template.name,
            description=exercise_template.description,
            type=exercise_template.type
        )

    def get_all_exercise_templates(self):
        return [
        {
            "name": "Fake Exercise  1",
            "description": "Description 1",
            "type": "a type",
            "id": 1
        },
        {
            "name": "Fake Exercise  2",
            "description": "Description 2",
            "type": "a type",
            "id": 2
        },
        {
            "name": "Fake Exercise  3",
            "description": "Description 3",
            "type": "a type",
            "id": 3
        },
    ]

    def get_one_exercise_template(self, exercise_template_id):
        return {
            "name": "fake exercise 1",
            "description": "fake description",
            "type": "fake type",
            "id": exercise_template_id,
        }

    def update_one_exercise_template(
        self,
        exercise_template_id: int,
        exercise_template: UpdateExerciseTemplate
    ):
        return {
            "name": exercise_template.name,
            "description": exercise_template.description,
            "type": exercise_template.type,
            "id": exercise_template_id
        }

    def delete_one_exercise_template(self, exercise_template_id: int):
        if exercise_template_id == 1:
            return {"message": "Exercise template deleted successfully!"}
        else:
            return {"message": "Failed to delete exercise template."}

def test_create_exercise_template():
   app.dependency_overrides[ExerciseTemplateRepo] = FakeExerciseTemplateRepo

   new_exercise_template = {
       "name": "new fake exercise",
       "description": "new exercise description",
       "type": "fake existing type",
   }

   response = client.post("/api/exercise_templates", json=new_exercise_template)
   data = response.json()
   assert response.status_code == 200
   assert data["name"] == new_exercise_template["name"]
   assert data["description"] == new_exercise_template["description"]


def test_get_all_exercise_templates():
    app.dependency_overrides[ExerciseTemplateRepo] = FakeExerciseTemplateRepo

    response = client.get("/api/exercise_templates")
    data = response.json()

    assert response.status_code == 200
    assert data == [
        {
            "name": "Fake Exercise  1",
            "description": "Description 1",
            "type": "a type",
            "id": 1
        },
        {
            "name": "Fake Exercise  2",
            "description": "Description 2",
            "type": "a type",
            "id": 2
        },
        {
            "name": "Fake Exercise  3",
            "description": "Description 3",
            "type": "a type",
            "id": 3
        },
    ]


def test_get_one_exercise_template():
    app.dependency_overrides[ExerciseTemplateRepo] = FakeExerciseTemplateRepo

    response = client.get("/api/exercise_templates/1")
    data = response.json()
    expected = {
            "name": "fake exercise 1",
            "description": "fake description",
            "type": "fake type",
            "id": 1,
        }
    assert response.status_code == 200
    assert data == expected

def test_update_one_exercise_template():
    app.dependency_overrides[ExerciseTemplateRepo] = FakeExerciseTemplateRepo

    updated_exercise_template = {
        "id": 1,
        "name": "Updated exercise",
        "description": "Updated description",
        "type": "Updated type"
    }

    response = client.put(
        "/api/exercise_templates/1",
        json=updated_exercise_template
    )

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == updated_exercise_template["name"]
    assert data["description"] == updated_exercise_template["description"]
    assert data["type"] == updated_exercise_template["type"]
    assert data["id"] == updated_exercise_template["id"]

def test_delete_one_exercise_template():
    app.dependency_overrides[ExerciseTemplateRepo] = FakeExerciseTemplateRepo

    response = client.delete("/api/exercise_templates/1")
    data = response.json()

    assert response.status_code == 200
    assert data == {"message": "Exercise template deleted successfully!"}

    response_fail = client.delete("/api/exercise_templates/1000")
    data_fail = response_fail.json()

    assert response_fail.status_code == 200
    assert data_fail == {"message": "Failed to delete exercise template."}
