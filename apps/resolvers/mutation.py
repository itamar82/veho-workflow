import logging

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from apps.db.entities import Pallet
from apps.resolvers.dtos import InductPackagesInputDto, StowPackagesInputDto
from apps.services import workflow_services
from apps.services.repository import WmsRepository
from apps.utils import api_response_handler, convert_kwargs_to_pydantic

mutation_type = MutationType()

logger = logging.getLogger(__name__)


@mutation_type.field("inductPackages")
@api_response_handler
@convert_kwargs_to_snake_case
@convert_kwargs_to_pydantic
def resolve_induct_packages_mutation(
    _, info: GraphQLResolveInfo, package_induction: InductPackagesInputDto
):
    repository = WmsRepository(info.context.session)

    warehouse = repository.load_warehouse_by_id(
        warehouse_id=package_induction.warehouse_id
    )
    if not warehouse:
        raise RuntimeError(
            f"Warehouse {package_induction.warehouse_id} not found",
        )

    packages = repository.load_packages_by_ids(
        warehouse_id=package_induction.warehouse_id,
        package_ids=package_induction.package_ids,
    )

    workflow_services.induct_packages(packages=packages)


@mutation_type.field("stowPackages")
@api_response_handler
@convert_kwargs_to_snake_case
@convert_kwargs_to_pydantic
def resolve_stow_packages_mutation(
    _, info: GraphQLResolveInfo, package_stow: StowPackagesInputDto
):
    repository = WmsRepository(info.context.session)

    warehouse = repository.load_warehouse_by_id(warehouse_id=package_stow.warehouse_id)
    if not warehouse:
        raise RuntimeError(f"Warehouse {package_stow.warehouse_id} not found")

    packages = repository.load_packages_by_ids(
        warehouse_id=package_stow.warehouse_id,
        package_ids=package_stow.package_ids,
    )

    if not packages:
        raise RuntimeError("No packages found to stow")

    pallet = repository.load_pallet_by_id(
        warehouse_id=package_stow.warehouse_id, pallet_id=package_stow.pallet_id
    )
    if not pallet:
        # create pallet
        pallet = Pallet(
            id=package_stow.pallet_id,
            warehouse_id=package_stow.warehouse_id,
            packages=[],
        )
        info.context.session.add(pallet)

    workflow_services.stow_packages(pallet=pallet, packages=packages)
