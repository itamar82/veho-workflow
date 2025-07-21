from sqlalchemy.orm import registry, relationship

from apps.db.entities import Location, Package, Pallet, Warehouse
from apps.db.schema import (
    locations_table,
    metadata,
    packages_table,
    pallets_table,
    warehouse_table,
)

mapper_registry = registry(metadata=metadata)


def initialize_mappers():
    mapper_registry.map_imperatively(
        Warehouse,
        warehouse_table,
        properties={"id": warehouse_table.c.id, "name": warehouse_table.c.name},
    )

    mapper_registry.map_imperatively(
        Location,
        locations_table,
        properties={
            "id": locations_table.c.id,
            "warehouse": relationship("Warehouse", uselist=False, lazy="joined"),
            "zone": locations_table.c.zone,
        },
    )

    mapper_registry.map_imperatively(
        Package,
        packages_table,
        properties={
            "id": packages_table.c.id,
            "warehouse": relationship("Warehouse", uselist=False, lazy="joined"),
            "received_timestamp": packages_table.c.received_timestamp,
            "status": packages_table.c.status,
            "pallet": relationship("Pallet", uselist=False, lazy="select"),
        },
    )

    mapper_registry.map_imperatively(
        Pallet,
        pallets_table,
        properties={
            "id": pallets_table.c.id,
            "warehouse": relationship("Warehouse", uselist=False, lazy="joined"),
            "packages": relationship(
                "Package", uselist=True, lazy="select", overlaps="pallet"
            ),
            "location": relationship("Location", uselist=False, lazy="joined"),
        },
    )


def start_mappers() -> None:
    """Initialize mappers if not already initialized"""
    if mapper_registry.mappers:
        # Mappers already initialized, just return
        return

    initialize_mappers()

    mapper_registry.configure()
