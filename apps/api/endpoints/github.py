import logging
from typing import Annotated

from fastapi import Body, Depends, Header

from apps.api import event_ingress_service
from apps.api.bootstrap import unit_of_work
from apps.api.endpoints import Endpoint
from apps.service_layer.unit_of_work import AbstractUnitOfWork

endpoint = Endpoint(prefix="/hooks")

logger = logging.getLogger(__name__)


@endpoint.router.post("/payload")
def handle_hook(
    hook_event: Annotated[str, Header(alias="X-GitHub-Event")],
    hook_delivery_id: Annotated[str, Header(alias="X-GitHub-Delivery")],
    payload: Annotated[dict, Body()],
    uow: Annotated[AbstractUnitOfWork, Depends(unit_of_work)],
):
    match hook_event:
        case "push":
            event_ingress_service.handle_push_event(
                uow, github_uuid=hook_delivery_id, payload=payload
            )
        case "repository":
            event_ingress_service.handle_repository_event(
                uow, github_uuid=hook_delivery_id, payload=payload
            )

        case "team":
            event_ingress_service.handle_team_event(
                uow, github_uuid=hook_delivery_id, payload=payload
            )

        case _:
            logger.error(
                f"Unsupported event type {hook_event}", extra={"payload": payload}
            )

    uow.commit()
