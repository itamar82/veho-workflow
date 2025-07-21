from datetime import datetime

from pydantic import BaseModel, Field

from apps.db.entities import Package, Pallet, Warehouse


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


class PackageDto(BaseModel):
    id: str
    warehouse_id: str
    received_timestamp: datetime | None
    status: str
    pallet_id: str


class PalletDto(BaseModel):
    id: str
    warehouse_id: str
    packages: list[PackageDto] = Field(default_factory=list)


def map_package_dto_from_entity(entity: Package) -> PackageDto:
    return PackageDto(
        id=entity.id,
        warehouse_id=entity.warehouse_id,
        received_timestamp=entity.received_timestamp,
        status=entity.status,
        pallet_id=entity.pallet_id,
    )


def map_pallet_dto_from_entity(entity: Pallet) -> PalletDto:
    return PalletDto(id=entity.id, warehouse_id=entity.warehouse_id)


def map_warehouse_dto_from_entity(entity: Warehouse) -> WarehouseDto:
    return WarehouseDto(id=entity.id, name=entity.name)
