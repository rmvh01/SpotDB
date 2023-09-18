from fastapi.testclient import TestClient
from main import app
from queries.metric_templates import (
    MetricTemplateIn,
    MetricTemplateOut,
    UpdateMetricTemplate,
    MetricTemplatesRepo,
)

client = TestClient(app)


class FakeMetricTemplatesRepo:

    def create_metric_template(self, metric_template: MetricTemplateIn):
        return MetricTemplateOut(
            id=1,
            name=metric_template.name,
            unit=metric_template.unit,
        )

    def get_all_metric_templates(self):
        return [
            {
                "id": 1,
                "name": "metric template 01",
                "unit": "metric unit",
            },
            {
                "id": 2,
                "name": "metric template 02",
                "unit": "metric unit",
            },
        ]

    def get_one_metric_template(
        self,
        metric_template_id: int,
    ):
        return {
            "id": metric_template_id,
            "name": "metric template 01",
            "unit": "metric unit",
        }

    def update_one_metric_template(
        self,
        metric_template_id: int,
        metric_template: UpdateMetricTemplate
    ):
        return {
            "id": metric_template_id,
            "name": metric_template.name,
            "unit": metric_template.unit,
        }

    def delete_one_metric_template(
        self,
        metric_template_id: int,
    ):
        if metric_template_id == 1:
            return {"message": "Metric template deleted successfully!"}
        else:
            return {"message": "Failed to delete metric template."}


def test_create_metric_template():
    app.dependency_overrides[MetricTemplatesRepo] = FakeMetricTemplatesRepo

    new_metric_template = {
        "name": "metric 01",
        "unit": "metric unit",
    }

    response = client.post("/api/metric_templates", json=new_metric_template)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == new_metric_template["name"]
    assert data["unit"] == new_metric_template["unit"]


def test_get_all_metric_templates():
    app.dependency_overrides[MetricTemplatesRepo] = FakeMetricTemplatesRepo

    response = client.get("/api/metric_templates")
    data = response.json()

    assert response.status_code == 200
    assert data == [
        {
            "id": 1,
            "name": "metric template 01",
            "unit": "metric unit",
        },
        {
            "id": 2,
            "name": "metric template 02",
            "unit": "metric unit",
        },
    ]

def test_get_one_metric_template():
    app.dependency_overrides[MetricTemplatesRepo] = FakeMetricTemplatesRepo

    response = client.get("/api/metric_templates/1")
    data = response.json()

    expected = {
        "id": 1,
        "name": "metric template 01",
        "unit": "metric unit",
    }
    assert response.status_code == 200
    assert data == expected

def test_update_one_metric_template():
    app.dependency_overrides[MetricTemplatesRepo] = FakeMetricTemplatesRepo

    new_template = {
        "id": 1,
        "name": "updated metric template 01",
        "unit": "updated metric unit",
    }

    response = client.put("/api/metric_templates/1", json=new_template)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == new_template["id"]
    assert data["name"] == new_template["name"]
    assert data["unit"] == new_template["unit"]

def test_delete_one_metric_template():
    app.dependency_overrides[MetricTemplatesRepo] = FakeMetricTemplatesRepo
    response = client.delete("/api/metric_templates/1")
    data = response.json()

    assert response.status_code == 200
    assert data == {"message": "Metric template deleted successfully!"}

    response_fail = client.delete("/api/metric_templates/2")
    data_fail = response_fail.json()

    assert response_fail.status_code == 200
    assert data_fail == {"message": "Failed to delete metric template."}
