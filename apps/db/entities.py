from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


@dataclass
class Warehouse:
    id: str
    name: str


@dataclass
class Pallet:
    id: str
    warehouse_id: str
    packages: list["Package"] = field(default_factory=list)
    location_id: str | None = None


class PackageStatus(StrEnum):
    PENDING = "pending"
    INDUCTED = "inducted"
    STOWED = "stowed"
    STAGED = "staged"
    PICKED = "picked"


@dataclass
class Package:
    id: str
    warehouse_id: str
    status: PackageStatus = PackageStatus.PENDING
    received_timestamp: datetime | None = None
    pallet: Pallet | None = None
