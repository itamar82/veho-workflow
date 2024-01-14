from datetime import datetime

from sqlalchemy import Column, DateTime, Index, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import registry

from apps.domain.models import PushEventEntity, RepositoryEventEntity, TeamEventEntity

mapper_registry = registry()
BaseEntity = mapper_registry.generate_base()


push_events_table = Table(
    "push_events",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto"),
    Column("github_uuid", String(30), nullable=False),
    Column("timestamp", DateTime(), nullable=False, default=datetime.utcnow),
    Column("pusher", String(30), nullable=False),
    Column("repository", String(50), nullable=False),
    Index("ix_push_events_pusher", "pusher"),
    Index("ix_push_events_repository", "repository"),
    UniqueConstraint("github_uuid", name="uix_push_events_github_uuid"),
)


mapper_registry.map_imperatively(
    PushEventEntity,
    push_events_table,
    properties={
        "id": push_events_table.c.id,
        "github_uuid": push_events_table.c.github_uuid,
        "timestamp": push_events_table.c.timestamp,
        "pusher": push_events_table.c.pusher,
        "repository": push_events_table.c.repository,
    },
)


repository_events_table = Table(
    "repository_events",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto"),
    Column("github_uuid", String(30), nullable=False),
    Column("timestamp", DateTime(), nullable=False, default=datetime.utcnow),
    Column("sender", String(30), nullable=False),
    Column("repository", String(50), nullable=False),
    Column("action", String(20), nullable=False),
    Index("ix_repository_events_repository", "repository"),
    UniqueConstraint("github_uuid", name="uix_repository_events_github_uuid"),
)

mapper_registry.map_imperatively(
    RepositoryEventEntity,
    repository_events_table,
    properties={
        "id": repository_events_table.c.id,
        "github_uuid": repository_events_table.c.github_uuid,
        "timestamp": repository_events_table.c.timestamp,
        "sender": repository_events_table.c.sender,
        "repository": repository_events_table.c.repository,
        "action": repository_events_table.c.action,
    },
)


team_events_table = Table(
    "team_events",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto"),
    Column("github_uuid", String(30), nullable=False),
    Column("timestamp", DateTime(), nullable=False, default=datetime.utcnow),
    Column("sender", String(30), nullable=False),
    Column("repository", String(50), nullable=False),
    Column("team", String(50), nullable=False),
    Column("action", String(20), nullable=False),
    Index("ix_team_events_repository", "repository"),
    UniqueConstraint("github_uuid", name="uix_team_events_github_uuid"),
)

mapper_registry.map_imperatively(
    TeamEventEntity,
    team_events_table,
    properties={
        "id": team_events_table.c.id,
        "github_uuid": team_events_table.c.github_uuid,
        "timestamp": team_events_table.c.timestamp,
        "sender": team_events_table.c.sender,
        "repository": team_events_table.c.repository,
        "team": team_events_table.c.team,
        "action": team_events_table.c.action,
    },
)


def start_mappers():
    mapper_registry.configure()
