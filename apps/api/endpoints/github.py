import logging
from typing import Annotated

from fastapi import Body, Header

from apps.api.endpoints import Endpoint

endpoint = Endpoint(prefix="/hooks")

logger = logging.getLogger(__name__)


@endpoint.router.post("/payload")
def handle_hook(
    hook_id: Annotated[str, Header(aliias="X-GitHub-Hook-ID")],
    hook_event: Annotated[str, Header(alias="X-GitHub-Event")],
    hook_delivery_id: Annotated[str, Header(alias="X-GitHub-Delivery")],
    payload: Annotated[dict, Body()],
):
    match hook_event:
        case "push":
            pass
        case "create":
            pass
        case "delete":
            pass

        case _:
            logger.error(
                f"Unsupported event type {hook_event}", extra={"payload": payload}
            )
