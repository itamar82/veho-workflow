"""Pytest configuration for CRM tests"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import apps.db
from apps.context import TransactionalGraphQLContext
from apps.db.orm import start_mappers
from apps.main import create_app


@pytest.fixture(scope="function")
def engine():
    """Create a fresh in-memory SQLite database for each test"""
    engine = create_engine("sqlite+pysqlite:///test.db", echo=True)
    # engine = create_engine(
    #     "sqlite+pysqlite:///:memory:",
    #     echo=True,
    #     connect_args={"check_same_thread": False},
    # )

    apps.db.engine = engine

    start_mappers()
    apps.db.orm.mapper_registry.metadata.create_all(bind=engine, checkfirst=True)
    yield engine
    apps.db.orm.mapper_registry.metadata.drop_all(bind=engine, checkfirst=True)


@pytest.fixture(scope="function")
def session(engine):
    """Create a database session for each test"""

    # prevent session commit and disposal but keep rollback
    TransactionalGraphQLContext.commit = lambda self: None
    TransactionalGraphQLContext._cleanup = lambda self: None

    with engine.connect() as connection:
        with connection.begin():
            with sessionmaker(
                bind=connection, autoflush=True, autocommit=False
            )() as session:
                apps.main.get_context_value = lambda req: TransactionalGraphQLContext(
                    request=req, session=session
                )
                yield session
                session.rollback()


@pytest.fixture(scope="function")
def api(session):
    app = create_app()

    yield app


@pytest.fixture(scope="function")
def client(api):
    """
    :param api: Dependency injected from the api fixture above
    """
    with TestClient(api) as client:
        yield client
