from typing import Callable

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

SessionFactory = Callable[..., Session]


class DatabaseManager:
    engine: Engine
    session_factory: SessionFactory

    @classmethod
    def init(cls):
        cls.engine = create_engine("sqlite+pysqlite:///./hooks.db", echo=True)
        cls.session_factory = sessionmaker(
            cls.engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False,
            future=True,
        )

    @classmethod
    def close(cls):
        cls.engine.dispose(close=True)
