from fastapi.testclient import TestClient
from main import app
from queries.exercise_templates import ExerciseTemplateRepo, ExerciseTemplateOut

client = TestClient(app)


class FakeExerciseTemplateRepo:
    # testing get all exercise templates
    def create_exercise_template(self, exercise_template):
        return ExerciseTemplateOut(
            id=999,
            name=exercise_template.name,
            description=exercise_template.description,
            type=exercise_template.type
        )


def test_create_exercise_template():
#    app.dependency_overrides
    pass
