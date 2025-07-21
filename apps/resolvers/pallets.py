from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.dataloaders import (
    LocationReferenceDataLoader,
    PackagesByPalletReferenceLoader,
    WarehouseReferenceLoader,
)
from apps.resolvers.dtos import PalletDto
from apps.services.repository import WmsRepository

pallet_type = ObjectType("Pallet")


@pallet_type.field("packages")
async def resolve_pallet_packages(representation: PalletDto, info: GraphQLResolveInfo):
    if PackagesByPalletReferenceLoader.CACHE_KEY() not in info.context:
        info.context[
            PackagesByPalletReferenceLoader.CACHE_KEY()
        ] = PackagesByPalletReferenceLoader(
            warehouse_id=representation.warehouse_id,
            repository=WmsRepository(session=info.context.session),
        )

    return await info.context[PackagesByPalletReferenceLoader.CACHE_KEY()].load(
        representation.id
    )


@pallet_type.field("warehouse")
async def resolve_package_warehouse(
    representation: PalletDto, info: GraphQLResolveInfo
):
    if WarehouseReferenceLoader.CACHE_KEY() not in info.context:
        info.context[WarehouseReferenceLoader.CACHE_KEY()] = WarehouseReferenceLoader(
            repository=WmsRepository(session=info.context.session)
        )

    return await info.context[WarehouseReferenceLoader.CACHE_KEY()].load(
        representation.warehouse_id
    )


@pallet_type.field("location")
async def resolve_pallet_location(representation: PalletDto, info: GraphQLResolveInfo):
    if LocationReferenceDataLoader.CACHE_KEY() not in info.context:
        info.context[
            LocationReferenceDataLoader.CACHE_KEY()
        ] = LocationReferenceDataLoader(
            warehouse_id=representation.warehouse_id,
            repository=WmsRepository(session=info.context.session),
        )

    return await info.context[LocationReferenceDataLoader.CACHE_KEY()].load(
        representation.location_id
    )
