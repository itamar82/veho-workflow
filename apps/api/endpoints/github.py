import logging
from typing import Annotated, Optional

from fastapi import BackgroundTasks, Body, Depends, Header

from apps.api.bootstrap import unit_of_work
from apps.api.endpoints import Endpoint
from apps.domain.models import EventEntityBase
from apps.service_layer import event_ingress_service, event_stream_analyzer
from apps.service_layer.unit_of_work import AbstractUnitOfWork

endpoint = Endpoint(prefix="/hooks")

logger = logging.getLogger(__name__)


@endpoint.router.post("/payload")
def handle_hook(
    hook_event: Annotated[str, Header(alias="X-GitHub-Event")],
    hook_delivery_id: Annotated[str, Header(alias="X-GitHub-Delivery")],
    payload: Annotated[dict, Body()],
    uow: Annotated[AbstractUnitOfWork, Depends(unit_of_work)],
    background_tasks: BackgroundTasks,
):
    event: Optional[EventEntityBase] = None

    match hook_event:
        case "push":
            event = event_ingress_service.handle_push_event(
                uow, github_uuid=hook_delivery_id, payload=payload
            )
        case "repository":
            event = event_ingress_service.handle_repository_event(
                uow, github_uuid=hook_delivery_id, payload=payload
            )

        case "team":
            event = event_ingress_service.handle_team_event(
                uow, github_uuid=hook_delivery_id, payload=payload
            )

        case _:
            logger.error(
                f"Unsupported event type {hook_event}", extra={"payload": payload}
            )

    uow.commit()
    if event:
        background_tasks.add_task(event_stream_analyzer.analyze_event, event)
