from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


@dataclass
class Warehouse:
    id: str
    name: str


@dataclass
class Location:
    id: str
    warehouse: Warehouse
    zone: str


@dataclass
class Pallet:
    id: str
    warehouse: Warehouse
    location: Location
    packages: list["Package"] = field(default_factory=list)
    stowed_timestamp: datetime | None = None


class PackageStatus(StrEnum):
    PENDING = "pending"
    INDUCTED = "inducted"
    STOWED = "stowed"
    STAGED = "staged"
    PICKED = "picked"


@dataclass
class Package:
    id: str
    warehouse: Warehouse
    status: PackageStatus = PackageStatus.PENDING
    received_timestamp: datetime | None = None
    pallet: Pallet | None = None
