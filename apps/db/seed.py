import uuid

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from .entities import Package, Warehouse, PackageStatus


def seed_db(engine: Engine):
    with Session(bind=engine, autoflush=True, autocommit=False) as session:
        warehouses = session.execute(select(Warehouse)).fetchall()
        if warehouses:
            return

        warehouses = [
            Warehouse(id=uuid.uuid4().hex, name="boston"),
            Warehouse(id=uuid.uuid4().hex, name="dallas"),
        ]

        session.add_all(warehouses)
        session.flush()

        warehouse_map = {warehouse.name: warehouse for warehouse in warehouses}

        packages = [
            Package(
                id=uuid.uuid4().hex,
                warehouse_id=warehouse_map["boston"].id,
                status=PackageStatus.PENDING,
                received_timestamp=None,
            )
            for _ in range(10)
        ]
        session.add_all(packages)
        session.flush()

        session.commit()
