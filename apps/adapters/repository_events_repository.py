import abc
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.domain.models import RepositoryEventEntity


class AbstractRepositoryEventsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: RepositoryEventEntity):
        pass

    @abc.abstractmethod
    def get_by_github_uuid(self, github_uuid: str) -> Optional[RepositoryEventEntity]:
        pass

    @abc.abstractmethod
    def get_repository_created_event(
        self, repository: str
    ) -> Optional[RepositoryEventEntity]:
        pass


class SqlAlchemyRepositoryEventsRepository(AbstractRepositoryEventsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_repository_created_event(
        self, repository: str
    ) -> Optional[RepositoryEventEntity]:
        entity = self.session.scalar(
            select(RepositoryEventEntity).where(
                RepositoryEventEntity.repository == repository,
                RepositoryEventEntity.action == "created",
            )
        )

        return entity

    def get_by_github_uuid(self, github_uuid: str) -> Optional[RepositoryEventEntity]:
        entity = self.session.scalar(
            select(RepositoryEventEntity).where(
                RepositoryEventEntity.github_uuid == github_uuid
            )
        )

        return entity

    def add(self, entity: RepositoryEventEntity):
        self.session.add(entity)
