from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EventEntityBase:
    github_uuid: str
    timestamp: datetime
    repository: str


@dataclass
class PushEventEntity(EventEntityBase):
    id: int = field(init=False)
    pusher: str


@dataclass
class RepositoryEventEntity(EventEntityBase):
    id: int = field(init=False)
    sender: str
    action: str


@dataclass
class TeamEventEntity(EventEntityBase):
    id: int = field(init=False)
    sender: str
    team: str
    action: str
