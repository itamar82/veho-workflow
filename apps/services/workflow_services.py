from datetime import UTC, datetime
from typing import Iterable

from apps.db.entities import Package, PackageStatus, Pallet
from apps.services.repository import WmsRepository


def induct_packages(packages: Iterable[Package]):
    for package in packages:
        if package.received_timestamp:
            raise RuntimeError(
                f"Package {package.id} already inducted",
            )

        package.received_timestamp = datetime.now(UTC)
        package.status = PackageStatus.INDUCTED


def stow_packages(
    pallet: Pallet, packages: Iterable[Package], repository: WmsRepository
):
    location = repository.load_location_by_id(
        warehouse_id=pallet.warehouse_id, location_id=pallet.location_id
    )
    if not location or location.zone not in ["RECEIVING"]:
        raise RuntimeError(f"Pallet {pallet.id} is not in receiving location")

    for package in packages:
        if not package.received_timestamp and package.status != PackageStatus.INDUCTED:
            raise RuntimeError(f"Package {package.id} has not been inducted")

        if package.pallet and package.pallet.id != pallet.id:
            raise RuntimeError(
                f"Package {package.id} already stowed in another pallet {package.pallet.id}"
            )
        elif package.pallet and package.pallet.id == pallet.id:
            continue

        pallet.packages.append(package)
        package.status = PackageStatus.STOWED

    pallet.stowed_timestamp = datetime.now(UTC)
