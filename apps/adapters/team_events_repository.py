import abc
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.domain.models import TeamEventEntity


class AbstractTeamEventsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: TeamEventEntity):
        pass

    @abc.abstractmethod
    def get_by_github_uuid(self, github_uuid: str) -> Optional[TeamEventEntity]:
        pass


class SqlAlchemyTeamEventsRepository(AbstractTeamEventsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_github_uuid(self, github_uuid: str) -> Optional[TeamEventEntity]:
        entity = self.session.scalar(
            select(TeamEventEntity).where(TeamEventEntity.github_uuid == github_uuid)
        )

        return entity

    def add(self, entity: TeamEventEntity):
        self.session.add(entity)
