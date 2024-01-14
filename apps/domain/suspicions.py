from datetime import datetime


class Suspicion:
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class SuspiciousCodePush(Suspicion):
    def __init__(self, repository: str, timestamp: datetime):
        super().__init__(f"Suspicious code push to '{repository}' at {timestamp}")


class SuspiciousTeamCreated(Suspicion):
    def __init__(self, team: str):
        super().__init__(f"Suspicious team '{team}' created")


class SuspiciousRepository(Suspicion):
    def __init__(self, repository: str, reason: str):
        super().__init__(f"Suspicious repository '{repository}': {reason}")
