from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from apps.adapters import orm
from apps.service_layer.unit_of_work import SqlAlchemyUnitOfWork, UnitOfWorkProvider
from apps.utilities.database import DatabaseManager


def _init_orm():
    DatabaseManager.init()
    orm.start_mappers()
    orm.mapper_registry.metadata.create_all(bind=DatabaseManager.engine)
    yield
    DatabaseManager.close()


class Container(DeclarativeContainer):
    _init_orm = providers.Resource(_init_orm)
    unit_of_work_provider = providers.Factory(
        UnitOfWorkProvider, uow_type=SqlAlchemyUnitOfWork
    )
