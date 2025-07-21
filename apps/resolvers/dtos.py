from datetime import datetime

from pydantic import BaseModel, Field

from apps.db.entities import Location, Package, Pallet, Warehouse


class ApiResponse(BaseModel):
    success: bool
    message: str | None = None


class InductPackagesInputDto(BaseModel):
    warehouse_id: str
    package_ids: list[str]


class StowPackagesInputDto(BaseModel):
    warehouse_id: str
    pallet_id: str
    package_ids: list[str]


class WarehouseDto(BaseModel):
    id: str
    name: str


class LocationDto(BaseModel):
    id: str
    warehouse: WarehouseDto
    zone: str


class PackageDto(BaseModel):
    id: str
    warehouse: WarehouseDto
    received_timestamp: datetime | None
    status: str
    pallet_id: str


class PalletDto(BaseModel):
    id: str
    warehouse: WarehouseDto
    location: LocationDto
    stowed_timestamp: datetime | None
    packages: list[PackageDto] = Field(default_factory=list)


def map_package_dto_from_entity(entity: Package) -> PackageDto:
    return PackageDto(
        id=entity.id,
        warehouse=map_warehouse_dto_from_entity(entity.warehouse),
        received_timestamp=entity.received_timestamp,
        status=entity.status,
        pallet_id=entity.pallet.id if entity.pallet else None,
    )


def map_pallet_dto_from_entity(entity: Pallet) -> PalletDto:
    return PalletDto(
        id=entity.id,
        warehouse=map_warehouse_dto_from_entity(entity.warehouse),
        stowed_timestamp=entity.stowed_timestamp,
        location=map_location_dto_from_entity(entity.location),
    )


def map_warehouse_dto_from_entity(entity: Warehouse) -> WarehouseDto:
    return WarehouseDto(id=entity.id, name=entity.name)


def map_location_dto_from_entity(entity: Location) -> LocationDto:
    return LocationDto(
        id=entity.id,
        warehouse=map_warehouse_dto_from_entity(entity.warehouse),
        zone=entity.zone,
    )
