from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.dataloaders import PackagesByPalletReferenceLoader
from apps.resolvers.dtos import PalletDto

pallet_type = ObjectType("Pallet")


@pallet_type.field("packages")
async def resolve_pallet_packages(representation: PalletDto, info: GraphQLResolveInfo):
    if PackagesByPalletReferenceLoader.CACHE_KEY() not in info.context:
        info.context[
            PackagesByPalletReferenceLoader.CACHE_KEY()
        ] = PackagesByPalletReferenceLoader(
            warehouse_id=representation.warehouse.id,
            repository=info.context.repository,
        )

    return await info.context[PackagesByPalletReferenceLoader.CACHE_KEY()].load(
        representation.id
    )
