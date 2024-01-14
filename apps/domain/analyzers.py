import abc
from datetime import time, timedelta
from typing import List

from apps.domain.models import PushEventEntity, RepositoryEventEntity, TeamEventEntity
from apps.domain.suspicions import Suspicion
from apps.service_layer.unit_of_work import AbstractUnitOfWork


class EventAnalyzerBase(abc.ABC):
    @abc.abstractmethod
    def analyze(self, event, uow: AbstractUnitOfWork) -> List[Suspicion]:
        pass


class SuspiciousTimestampPushEventAnalyzer(EventAnalyzerBase):
    def __init__(self, window_start: time, window_end: time):
        super().__init__()
        self.window_start = window_start
        self.window_end = window_end

    def analyze(
        self, event: PushEventEntity, uow: AbstractUnitOfWork
    ) -> List[Suspicion]:
        suspicions: List[Suspicion] = []

        if self.window_start <= event.timestamp.time() <= self.window_end:
            suspicions.append(
                Suspicion(
                    f"Suspicious code push to repository '{event.repository}' at {event.timestamp}"
                )
            )

        return suspicions


class SuspiciousTeamNameCreatedEventAnalyzer(EventAnalyzerBase):
    def __init__(self, starts_with: str):
        super().__init__()
        self.starts_with = starts_with.lower()

    def analyze(
        self, event: TeamEventEntity, uow: AbstractUnitOfWork
    ) -> List[Suspicion]:
        suspicions: List[Suspicion] = []

        if event.action != "created":
            return suspicions

        if event.team.lower().startswith(self.starts_with):
            suspicions.append(
                Suspicion(
                    f"Suspicious team name '{event.team}' added to repository '{event.repository}' at {event.timestamp}"
                )
            )

        return suspicions


class SuspiciousRepositoryLifetimeEventAnalyzer(EventAnalyzerBase):
    def __init__(self, lifetime: timedelta):
        super().__init__()
        self.lifetime = lifetime

    def analyze(
        self, event: RepositoryEventEntity, uow: AbstractUnitOfWork
    ) -> List[Suspicion]:
        suspicions: List[Suspicion] = []
        if event.action != "deleted":
            return suspicions

        repository_created_event = uow.repository_events.get_repository_created_event(
            event.repository
        )
        if (
            repository_created_event
            and event.timestamp - repository_created_event.timestamp < self.lifetime
        ):
            suspicions.append(
                Suspicion(
                    f"Suspicious repository lifetime for repository '{event.repository}' at {repository_created_event.timestamp} - {event.timestamp}"
                )
            )

        return suspicions
