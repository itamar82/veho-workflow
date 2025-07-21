from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from .entities import Location, Package, PackageStatus, Warehouse


def seed_db(engine: Engine):
    with Session(bind=engine, autoflush=True, autocommit=False) as session:
        warehouses = session.execute(select(Warehouse)).fetchall()
        if warehouses:
            return

        warehouses = [
            Warehouse(id="wh_1", name="boston"),
            Warehouse(id="wh_2", name="dallas"),
        ]

        locations = [
            Location(id="loc1", warehouse=warehouses[0], zone="RECEIVING"),
            Location(id="loc2", warehouse=warehouses[0], zone="STORAGE"),
        ]

        session.add_all(warehouses)
        session.add_all(locations)
        session.flush()

        warehouse_map = {warehouse.name: warehouse for warehouse in warehouses}

        packages = [
            Package(
                id=f"pkg_{i}",
                warehouse=warehouse_map["boston"],
                status=PackageStatus.PENDING,
                received_timestamp=None,
            )
            for i in range(10)
        ]
        session.add_all(packages)
        session.flush()

        session.commit()
