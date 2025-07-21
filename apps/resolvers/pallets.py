from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.dataloaders import PackagesByPalletReferenceLoader
from apps.resolvers.dtos import PalletDto
from apps.services.repository import WmsRepository

pallet_type = ObjectType("Pallet")


@pallet_type.field("packages")
async def resolve_pallet_packages(representation: PalletDto, info: GraphQLResolveInfo):
    if PackagesByPalletReferenceLoader.CACHE_KEY() not in info.context:
        info.context[
            PackagesByPalletReferenceLoader.CACHE_KEY()
        ] = PackagesByPalletReferenceLoader(
            warehouse_id=representation.warehouse.id,
            repository=WmsRepository(session=info.context.session),
        )

    return await info.context[PackagesByPalletReferenceLoader.CACHE_KEY()].load(
        representation.id
    )
