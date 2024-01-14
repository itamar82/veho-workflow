from datetime import datetime

from apps.domain.models import PushEventEntity, RepositoryEventEntity, TeamEventEntity
from apps.service_layer.unit_of_work import AbstractUnitOfWork


def handle_push_event(
    uow: AbstractUnitOfWork, github_uuid: str, payload: dict
) -> PushEventEntity:
    event = PushEventEntity(
        github_uuid=github_uuid,
        repository=payload["repository"]["name"],
        timestamp=datetime.utcnow(),
        pusher=payload["pusher"]["name"],
    )

    if not uow.push_events.get_by_github_uuid(github_uuid):
        uow.push_events.add(event)

    return event


def handle_repository_event(
    uow: AbstractUnitOfWork, github_uuid: str, payload: dict
) -> RepositoryEventEntity:
    event = RepositoryEventEntity(
        github_uuid=github_uuid,
        repository=payload["repository"]["name"],
        timestamp=datetime.utcnow(),
        sender=payload["sender"]["name"],
        action=payload["action"],
    )

    if not uow.repository_events.get_by_github_uuid(github_uuid):
        uow.repository_events.add(event)

    return event


def handle_team_event(
    uow: AbstractUnitOfWork, github_uuid: str, payload: dict
) -> TeamEventEntity:
    event = TeamEventEntity(
        github_uuid=github_uuid,
        repository=payload["repository"]["name"],
        timestamp=datetime.utcnow(),
        sender=payload["sender"]["name"],
        action=payload["action"],
        team=payload["team"]["name"],
    )

    if not uow.team_events.get_by_github_uuid(github_uuid):
        uow.team_events.add(event)

    return event
