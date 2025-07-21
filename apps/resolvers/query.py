import logging

from ariadne import ObjectType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from apps.resolvers.dtos import map_package_dto_from_entity, map_pallet_dto_from_entity
from apps.services.repository import WmsRepository

query_type = ObjectType("Query")

logger = logging.getLogger(__name__)


@query_type.field("getPackagesByIds")
@convert_kwargs_to_snake_case
def resolve_get_packages_by_ids(
    _, info: GraphQLResolveInfo, warehouse_id: str, package_ids: list[str]
):
    repository = WmsRepository(session=info.context.session)

    packages = repository.load_packages_by_ids(
        warehouse_id=warehouse_id, package_ids=package_ids
    )

    results = [map_package_dto_from_entity(p) for p in packages]

    return results


@query_type.field("getPalletsByIds")
@convert_kwargs_to_snake_case
def resolve_get_pallets_by_ids(
    _, info: GraphQLResolveInfo, warehouse_id: str, pallet_ids: list[str]
):
    repository = WmsRepository(session=info.context.session)

    pallets = repository.load_pallets_by_ids(
        warehouse_id=warehouse_id, pallet_ids=pallet_ids
    )

    return [map_pallet_dto_from_entity(p) for p in pallets]


@query_type.field("getPalletsByLocation")
@convert_kwargs_to_snake_case
def resolve_get_pallets_by_location(
    _, info: GraphQLResolveInfo, warehouse_id: str, location_id: str
):
    repository = WmsRepository(session=info.context.session)

    pallets = repository.load_pallets_by_location(
        warehouse_id=warehouse_id, location_id=location_id
    )

    return [map_pallet_dto_from_entity(p) for p in pallets]
