import itertools
import logging
from datetime import time, timedelta

from dependency_injector.wiring import Provide, inject

from apps.domain import analyzers
from apps.domain.models import (
    EventEntityBase,
    PushEventEntity,
    RepositoryEventEntity,
    TeamEventEntity,
)
from apps.service_layer.unit_of_work import UnitOfWorkProvider

# can define these analyzers in db or something later
_push_event_analyzers = [
    analyzers.SuspiciousTimestampPushEventAnalyzer(
        window_start=time(hour=14), window_end=time(hour=16)
    )
]

_team_event_analyzers = [
    analyzers.SuspiciousTeamNameCreatedEventAnalyzer(starts_with="hacker")
]

_repository_event_analyzers = [
    analyzers.SuspiciousRepositoryLifetimeEventAnalyzer(lifetime=timedelta(minutes=10))
]


logger = logging.getLogger(__name__)


@inject
def analyze_event(
    event: EventEntityBase,
    unit_of_work_provider: UnitOfWorkProvider = Provide["unit_of_work_provider"],
):
    with unit_of_work_provider.get_unit_of_work() as uow:
        if isinstance(event, PushEventEntity):
            suspicions = itertools.chain.from_iterable(
                [analyzer.analyze(event, uow) for analyzer in _push_event_analyzers]
            )
        elif isinstance(event, TeamEventEntity):
            suspicions = itertools.chain.from_iterable(
                [analyzer.analyze(event, uow) for analyzer in _team_event_analyzers]
            )
        elif isinstance(event, RepositoryEventEntity):
            suspicions = itertools.chain.from_iterable(
                [
                    analyzer.analyze(event, uow)
                    for analyzer in _repository_event_analyzers
                ]
            )

        for suspicion in suspicions:
            logger.warning(suspicion, extra={"event": event})
