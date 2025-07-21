from typing import Iterable, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apps.db.entities import Location, Package, Pallet, Warehouse


class WmsRepository:
    def __init__(self, session: Session):
        self.session = session

    def load_warehouses_by_ids(
        self, warehouse_ids: Iterable[str]
    ) -> Sequence[Warehouse]:
        warehouses = (
            self.session.execute(
                select(Warehouse).where(Warehouse.id.in_(warehouse_ids))
            )
            .scalars()
            .fetchall()
        )

        return warehouses

    def load_warehouse_by_id(self, warehouse_id: str) -> Warehouse | None:
        warehouse = self.session.execute(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        ).scalar_one_or_none()

        return warehouse

    def load_packages_by_ids(
        self, warehouse_id: str, package_ids: Iterable[str]
    ) -> Sequence[Package]:
        packages = (
            self.session.execute(
                select(Package).where(
                    Package.warehouse_id == warehouse_id,
                    Package.id.in_(package_ids),
                )
            )
            .scalars()
            .fetchall()
        )

        return packages

    def load_packages_by_pallet_ids(
        self, warehouse_id: str, pallet_ids: Iterable[str]
    ) -> Sequence[Package]:
        packages = (
            self.session.execute(
                select(Package).where(
                    Package.warehouse_id == warehouse_id,
                    Package.pallet_id.in_(pallet_ids),
                )
            )
            .scalars()
            .fetchall()
        )

        return packages

    def load_pallets_by_ids(
        self, warehouse_id: str, pallet_ids: Iterable[str]
    ) -> Sequence[Pallet]:
        pallets = (
            self.session.execute(
                select(Pallet).where(
                    Pallet.warehouse_id == warehouse_id,
                    Pallet.id.in_(pallet_ids),
                )
            )
            .scalars()
            .fetchall()
        )

        return pallets

    def load_pallets_by_package_ids(
        self, warehouse_id: str, package_ids: Iterable[str]
    ) -> Sequence[Pallet]:
        pallets = (
            self.session.execute(
                select(Pallet)
                .join(Package)
                .where(
                    Pallet.warehouse_id == warehouse_id,
                    Package.id.in_(package_ids),
                )
            )
            .scalars()
            .fetchall()
        )

        return pallets

    def load_pallet_by_id(self, warehouse_id: str, pallet_id: str) -> Pallet | None:
        pallets = self.session.execute(
            select(Pallet).where(
                Pallet.warehouse_id == warehouse_id, Pallet.id == pallet_id
            )
        ).scalar_one_or_none()

        return pallets

    def get_locations_by_zone(self, warehouse_id: str, zone: str) -> Sequence[Location]:
        locations = (
            self.session.execute(
                select(Location).where(
                    Location.warehouse_id == warehouse_id,
                    func.lower(Location.zone) == zone.lower(),
                )
            )
            .scalars()
            .fetchall()
        )

        return locations

    def load_pallets_by_location(
        self, warehouse_id: str, location_id: str
    ) -> Sequence[Pallet]:
        pallets = (
            self.session.execute(
                select(Pallet).where(
                    Pallet.warehouse_id == warehouse_id,
                    func.lower(Pallet.location_id) == location_id.lower(),
                )
            )
            .scalars()
            .fetchall()
        )

        return pallets
