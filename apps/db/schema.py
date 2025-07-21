from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)

metadata = MetaData()


warehouse_table = Table(
    "warehouses",
    metadata,
    Column("id", String(30), primary_key=True),
    Column("name", String(30), nullable=False, unique=True),
    UniqueConstraint("name"),
)

locations_table = Table(
    "locations",
    metadata,
    Column("id", String(30), primary_key=True),
    Column("warehouse_id", String(30), ForeignKey("warehouses.id"), nullable=False),
    Column("zone", String(30), nullable=False),
)

pallets_table = Table(
    "pallets",
    metadata,
    Column("id", String(30), primary_key=True),
    Column("warehouse_id", String(30), ForeignKey("warehouses.id"), nullable=False),
    Column("location_id", String(30), ForeignKey("locations.id"), nullable=True),
    UniqueConstraint("warehouse_id", "id"),
)

packages_table = Table(
    "packages",
    metadata,
    Column("id", String(30), primary_key=True),
    Column("warehouse_id", String(30), ForeignKey("warehouses.id"), nullable=False),
    Column("received_timestamp", DateTime(), nullable=True),
    Column("status", String(30), nullable=True),
    Column("pallet_id", String(30), ForeignKey("pallets.id"), nullable=True),
    UniqueConstraint("warehouse_id", "id"),
)
