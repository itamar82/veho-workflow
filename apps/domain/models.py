from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PushEventEntity:
    id: int = field(init=False)
    github_uuid: str
    timestamp: datetime
    pusher: str
    repository: str


@dataclass
class RepositoryEventEntity:
    id: int = field(init=False)
    github_uuid: str
    timestamp: datetime
    sender: str
    repository: str
    action: str


@dataclass
class TeamEventEntity:
    id: int = field(init=False)
    github_uuid: str
    timestamp: datetime
    sender: str
    repository: str
    team: str
    action: str
