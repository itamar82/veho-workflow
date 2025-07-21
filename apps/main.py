import logging
from contextlib import asynccontextmanager
from os import getenv
from typing import Any

from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLHTTPHandler
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.requests import Request

from apps import db
from apps.context import TransactionalGraphQLContext
from apps.db import orm
from apps.schema import schema

logger = logging.getLogger(__name__)


def get_context_value(request: Request):
    context = TransactionalGraphQLContext(
        request=request,
        session=Session(bind=db.engine, autoflush=False, autocommit=False),
    )
    return context


class TransactionalGraphQL(GraphQLHTTPHandler):
    async def graphql_http_server(self, request: Request) -> Any:
        """Override to wrap request in transaction context"""
        context = get_context_value(request)

        # Enter transaction context
        with context:
            # Temporarily store context in request state
            request.state.graphql_context = context

            try:
                # Process GraphQL request
                result = await super().graphql_http_server(request)
                return result
            except Exception as e:
                # Exception will trigger rollback in context manager
                logger.error(f"GraphQL request failed: {e}")
                raise


def create_app():
    app = FastAPI(
        title="WMS API",
        description="",
        lifespan=lifespan,
        debug=bool(getenv("DEBUG", True)),
    )

    app.mount(
        "/graphql",
        GraphQL(
            schema=schema,
            debug=True,
            http_handler=TransactionalGraphQL(),
            context_value=lambda request, _: request.state.graphql_context,
        ),
    )

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        orm.start_mappers()

        if bool(getenv("SEED_DB", True)):
            orm.mapper_registry.metadata.drop_all(bind=db.engine, checkfirst=True)
            orm.mapper_registry.metadata.create_all(bind=db.engine, checkfirst=True)

            from apps.db.seed import seed_db

            seed_db(db.engine)

        yield

        db.engine.dispose(close=True)
    except Exception as e:
        logger.exception("oops", exc_info=e)
