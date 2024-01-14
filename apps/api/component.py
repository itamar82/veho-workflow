import logging
from contextlib import asynccontextmanager
from os import getenv
from typing import List

from fastapi import FastAPI

from apps.api.dependencies import Container
from apps.api.endpoints import Endpoint, github

ENDPOINTS: List[Endpoint] = [github.endpoint]

logger = logging.getLogger(__name__)


def create_app():
    app = FastAPI(
        title="Github Webhook Processor API",
        description="Consumes webhooks from Github for anomaly detection",
        lifespan=lifespan,
        debug=bool(getenv("DEBUG", False)),
    )

    container = Container()
    container.wire(packages=["apps.api", "apps.service_layer", "apps.utilities"])
    app.state.container = container

    add_routes(app)

    return app


def add_routes(app: FastAPI):
    for endpoint in ENDPOINTS:
        app.include_router(endpoint.router, prefix=endpoint.prefix)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.container.init_resources()

        yield

        app.state.container.shutdown_resources()
    except Exception as e:
        logger.exception("oops", exc_info=e)
