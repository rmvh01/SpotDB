from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from queries.exercises.metric_templates import (
    MetricTemplateIn,
    MetricTemplateOut,
    UpdateMetricTemplate,
    MetricTemplatesRepo,
    Error,
)

from typing import List, Union

router = APIRouter()

@router.post(
    "/api/metric_templates",
    response_model=MetricTemplateOut,
    tags=["Metric Templates"]
)
def create_metric_template(
    metric_template: MetricTemplateIn,
    repo: MetricTemplatesRepo = Depends(),
):
    """
    The unit needs to a string with length < 11
    """
    return repo.create_metric_template(
        metric_template=metric_template,
    )


@router.get(
    "/api/metric_templates",
    response_model=Union[List[MetricTemplateOut], Error],
    tags=["Metric Templates"]
)
def get_all_metric_templates(
    repo: MetricTemplatesRepo = Depends(),
):
    return repo.get_all_metric_templates()


@router.get(
    "/api/metric_templates/{metric_template_id}",
    response_model=Union[MetricTemplateOut, Error],
    tags=["Metric Templates"]
)
def get_one_metric_template(
    metric_template_id: int,
    repo: MetricTemplatesRepo = Depends()
):
    metric_template = repo.get_one_metric_template(metric_template_id)
    if metric_template:
        return metric_template
    else:
        raise HTTPException(status_code=404, detail="Metric template not found")


@router.put(
    "/api/metric_templates/{metric_template_id}",
    response_model=Union[MetricTemplateOut, Error],
    tags=["Metric Templates"],
)
def update_one_metric_template(
    metric_template_id: int,
    metric_template: UpdateMetricTemplate,
    repo: MetricTemplatesRepo = Depends(),
):
    result = repo.update_one_metric_template(metric_template_id, metric_template)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="Metric template not found or update failed."
        )


@router.delete(
    "/api/metric_templates/{metric_template_id}",
    response_model=dict,
    tags=["Metric Templates"]
)
def delete_one_metric_template(
    metric_template_id: int,
    repo: MetricTemplatesRepo = Depends(),
):
    return repo.delete_one_metric_template(metric_template_id)
