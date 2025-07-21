from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.dataloaders import PalletReferenceLoader
from apps.resolvers.dtos import PackageDto

package_type = ObjectType("Package")


@package_type.field("pallet")
async def resolve_package_pallet(representation: PackageDto, info: GraphQLResolveInfo):
    if PalletReferenceLoader.CACHE_KEY() not in info.context:
        info.context[PalletReferenceLoader.CACHE_KEY()] = PalletReferenceLoader(
            warehouse_id=representation.warehouse.id,
            repository=info.context.repository,
        )

    return await info.context[PalletReferenceLoader.CACHE_KEY()].load(
        representation.pallet_id
    )
