import abc
from typing import Type

from sqlalchemy.orm import Session

from apps.adapters import (
    push_events_repository,
    repository_events_repository,
    team_events_repository,
)
from apps.utilities.database import DatabaseManager


class AbstractUnitOfWork(abc.ABC):
    push_events: push_events_repository.AbstractPushEventsRepository
    repository_events: repository_events_repository.AbstractRepositoryEventsRepository
    team_events: team_events_repository.AbstractTeamEventsRepository

    @abc.abstractmethod
    def __enter__(self):
        pass

    def __exit__(self, *args):  # (2)
        self.rollback()  # (4)

    @abc.abstractmethod
    def commit(self):  # (3)
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):  # (4)
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    _session: Session

    def __init__(self):
        self._session = DatabaseManager.session_factory()
        self.push_events = push_events_repository.SqlAlchemyPushEventsRepository(
            self._session
        )
        self.repository_events = (
            repository_events_repository.SqlAlchemyRepositoryEventsRepository(
                session=self._session
            )
        )
        self.team_events = team_events_repository.SqlAlchemyTeamEventsRepository(
            session=self._session
        )

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    @property
    def session(self):
        return self._session

    def commit(self):  # (4)
        self._session.commit()

    def rollback(self):  # (4)
        self._session.rollback()


class UnitOfWorkProvider:
    def __init__(self, uow_type: Type[AbstractUnitOfWork]):
        self.uow_type = uow_type

    def get_unit_of_work(self):
        return self.uow_type()
