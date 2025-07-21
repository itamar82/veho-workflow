from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.dataloaders import PalletReferenceLoader, WarehouseReferenceLoader
from apps.resolvers.dtos import PackageDto
from apps.services.repository import WmsRepository

package_type = ObjectType("Package")


@package_type.field("pallet")
async def resolve_package_pallet(representation: PackageDto, info: GraphQLResolveInfo):
    if PalletReferenceLoader.CACHE_KEY() not in info.context:
        info.context[PalletReferenceLoader.CACHE_KEY()] = PalletReferenceLoader(
            warehouse_id=representation.warehouse_id,
            repository=WmsRepository(session=info.context.session),
        )

    return await info.context[PalletReferenceLoader.CACHE_KEY()].load(
        representation.pallet_id
    )


@package_type.field("warehouse")
async def resolve_package_warehouse(
    representation: PackageDto, info: GraphQLResolveInfo
):
    if WarehouseReferenceLoader.CACHE_KEY() not in info.context:
        info.context[WarehouseReferenceLoader.CACHE_KEY()] = WarehouseReferenceLoader(
            repository=WmsRepository(session=info.context.session)
        )

    return await info.context[WarehouseReferenceLoader.CACHE_KEY()].load(
        representation.warehouse_id
    )
