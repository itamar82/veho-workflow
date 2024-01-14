import logging
from contextlib import asynccontextmanager
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
        debug=True,
    )

    container = Container()
    container.wire(packages=["apps.api"])
    app.state.container = container

    add_routes(app)

    return app


def add_routes(app: FastAPI):
    for endpoint in ENDPOINTS:
        app.include_router(endpoint.router, prefix=endpoint.prefix)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await app.state.container.init_resources()

    yield

    # await app.state.container.shutdown_resources()
