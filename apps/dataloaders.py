from itertools import groupby
from typing import Sequence

from aiodataloader import DataLoader
from requests import Session

from apps.resolvers.dtos import (
    map_location_dto_from_entity,
    map_package_dto_from_entity,
    map_pallet_dto_from_entity,
    map_warehouse_dto_from_entity,
)
from apps.services.repository import WmsRepository


class PalletReferenceLoader(DataLoader):
    _warehouse_id: str
    _session: Session

    @staticmethod
    def CACHE_KEY():  # noqa: N802
        return "PACKAGE_REFERENCE_LOADER"

    def __init__(self, warehouse_id: str, repository: WmsRepository):
        super().__init__()
        self._warehouse_id = warehouse_id
        self._repository = repository

    async def batch_load_fn(self, keys: Sequence[str]):
        packages = self._repository.load_pallets_by_ids(
            warehouse_id=self._warehouse_id, pallet_ids=keys
        )

        pallets_by_id = {p.id: p for p in packages}

        return [
            (
                map_pallet_dto_from_entity(pallets_by_id.get(k))
                if k in pallets_by_id
                else None
            )
            for k in keys
        ]


class PackagesByPalletReferenceLoader(DataLoader):
    _warehouse_id: str
    _session: Session

    @staticmethod
    def CACHE_KEY():  # noqa: N802
        return "PACKAGES_BY_PALLET_REFERENCE_LOADER"

    def __init__(self, warehouse_id: str, repository: WmsRepository):
        super().__init__()
        self._warehouse_id = warehouse_id
        self._repository = repository

    async def batch_load_fn(self, keys: Sequence[str | None]):
        packages = self._repository.load_packages_by_pallet_ids(
            warehouse_id=self._warehouse_id, pallet_ids=keys
        )

        packages_by_pallet_id = {
            key: [map_package_dto_from_entity(item) for item in group]
            for key, group in groupby(packages, lambda p: p.pallet_id)
        }

        return [
            packages_by_pallet_id.get(k) if k in packages_by_pallet_id else []
            for k in keys
        ]


class WarehouseReferenceLoader(DataLoader):
    _session: Session

    @staticmethod
    def CACHE_KEY():  # noqa: N802
        return "WAREHOUSE_REFERENCE_LOADER"

    def __init__(self, repository: WmsRepository):
        super().__init__()
        self._repository = repository

    async def batch_load_fn(self, keys: Sequence[str]):
        warehouses = self._repository.load_warehouses_by_ids(warehouse_ids=keys)

        warehouses_by_id = {w.id: w for w in warehouses}

        return [map_warehouse_dto_from_entity(warehouses_by_id.get(k)) for k in keys]


class LocationReferenceDataLoader(DataLoader):
    _session: Session

    @staticmethod
    def CACHE_KEY():  # noqa: N802
        return "LOCATION_REFERENCE_LOADER"

    def __init__(self, warehouse_id: str, repository: WmsRepository):
        super().__init__()
        self._warehouse_id = warehouse_id
        self._repository = repository

    async def batch_load_fn(self, keys: Sequence[str]):
        locations = self._repository.load_locations_by_ids(
            warehouse_id=self._warehouse_id, location_ids=keys
        )

        locations_by_id = {loc.id: loc for loc in locations}

        return [map_location_dto_from_entity(locations_by_id.get(k)) for k in keys]
