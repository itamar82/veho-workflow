from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.dataloaders import WarehouseReferenceLoader
from apps.resolvers.dtos import LocationDto
from apps.services.repository import WmsRepository

location_type = ObjectType("Location")


@location_type.field("warehouse")
async def resolve_package_warehouse(
    representation: LocationDto, info: GraphQLResolveInfo
):
    if WarehouseReferenceLoader.CACHE_KEY() not in info.context:
        info.context[WarehouseReferenceLoader.CACHE_KEY()] = WarehouseReferenceLoader(
            repository=WmsRepository(session=info.context.session)
        )

    return await info.context[WarehouseReferenceLoader.CACHE_KEY()].load(
        representation.warehouse_id
    )
