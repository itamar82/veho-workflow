from apps.service_layer.unit_of_work import SqlAlchemyUnitOfWork


def unit_of_work():
    with SqlAlchemyUnitOfWork() as session:
        yield session
