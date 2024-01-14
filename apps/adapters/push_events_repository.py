import abc
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.domain.models import PushEventEntity


class AbstractPushEventsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: PushEventEntity):
        pass

    @abc.abstractmethod
    def get_by_github_uuid(self, github_uuid: str) -> Optional[PushEventEntity]:
        pass


class SqlAlchemyPushEventsRepository(AbstractPushEventsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_github_uuid(self, github_uuid: str) -> Optional[PushEventEntity]:
        entity = self.session.scalar(
            select(PushEventEntity).where(PushEventEntity.github_uuid == github_uuid)
        )

        return entity

    def add(self, entity: PushEventEntity):
        self.session.add(entity)
