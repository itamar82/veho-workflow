from apps.db.entities import Location, Package, PackageStatus, Pallet, Warehouse


class TestMutationResolvers:
    """Integration tests for mutation resolvers"""

    def test_induct_packages_success(self, client, session):
        """Test successful package induction"""
        # First, create test packages
        warehouse = Warehouse(id="test_wh", name="Test Warehouse")
        package1 = Package(
            id="test_pkg1",
            warehouse=warehouse,
            status=PackageStatus.PENDING,
            received_timestamp=None,
        )
        package2 = Package(
            id="test_pkg2",
            warehouse=warehouse,
            status=PackageStatus.PENDING,
            received_timestamp=None,
        )

        session.add_all([warehouse, package1, package2])
        session.flush()

        mutation = """
        mutation InductPackages($packageInduction: PackageInductionInput!) {
            inductPackages(packageInduction: $packageInduction) {
                success
                message
            }
        }
        """

        variables = {
            "packageInduction": {
                "warehouseId": warehouse.id,
                "packageIds": [p.id for p in [package1, package2]],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["inductPackages"]
        assert response["success"] is True

        # Verify packages were updated
        updated_packages = (
            session.query(Package)
            .filter(Package.id.in_(["test_pkg1", "test_pkg2"]))
            .all()
        )

        for pkg in updated_packages:
            assert pkg.status == PackageStatus.INDUCTED.value
            assert pkg.received_timestamp is not None

    def test_induct_packages_warehouse_not_found(self, client):
        """Test induction with non-existent warehouse"""
        mutation = """
        mutation InductPackages($packageInduction: PackageInductionInput!) {
            inductPackages(packageInduction: $packageInduction) {
                success
                message
            }
        }
        """

        variables = {
            "packageInduction": {
                "warehouseId": "nonexistent_wh",
                "packageIds": ["pkg1", "pkg2"],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["inductPackages"]
        assert response["success"] is False
        assert "Warehouse nonexistent_wh not found" in response["message"]

    def test_induct_packages_already_inducted(self, client, session):
        """Test induction of already inducted packages"""
        from datetime import UTC, datetime

        # Create already inducted package
        warehouse = Warehouse(id="test_wh2", name="Test Warehouse 2")
        package = Package(
            id="test_pkg_inducted",
            warehouse=warehouse,
            status=PackageStatus.INDUCTED,
            received_timestamp=datetime.now(UTC),
        )

        session.add_all([warehouse, package])
        session.flush()

        mutation = """
        mutation InductPackages($packageInduction: PackageInductionInput!) {
            inductPackages(packageInduction: $packageInduction) {
                success
                message
            }
        }
        """

        variables = {
            "packageInduction": {
                "warehouseId": warehouse.id,
                "packageIds": [package.id],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["inductPackages"]
        assert response["success"] is False
        assert "already inducted" in response["message"]

    def test_stow_packages_success(self, client, session):
        """Test successful package stowing"""
        from datetime import UTC, datetime

        # Create test data
        warehouse = Warehouse(id="test_wh3", name="Test Warehouse 3")
        location = Location(id="loc1", warehouse=warehouse, zone="RECEIVING")
        package1 = Package(
            id="test_pkg_stow1",
            warehouse=warehouse,
            status=PackageStatus.INDUCTED,
            received_timestamp=datetime.now(UTC),
        )
        package2 = Package(
            id="test_pkg_stow2",
            warehouse=warehouse,
            status=PackageStatus.INDUCTED,
            received_timestamp=datetime.now(UTC),
        )

        session.add_all([warehouse, location, package1, package2])
        session.flush()

        mutation = """
        mutation StowPackages($packageStow: PackageStowInput!) {
            stowPackages(packageStow: $packageStow) {
                success
                message
            }
        }
        """

        variables = {
            "packageStow": {
                "warehouseId": warehouse.id,
                "palletId": "test_pallet",
                "packageIds": [p.id for p in [package1, package2]],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["stowPackages"]
        assert response["success"] is True

        # Verify pallet was created and packages were assigned
        pallet = session.query(Pallet).filter(Pallet.id == "test_pallet").first()

        assert pallet is not None
        assert len(pallet.packages) == 2

        package_ids = [pkg.id for pkg in pallet.packages]
        assert "test_pkg_stow1" in package_ids
        assert "test_pkg_stow2" in package_ids

    def test_stow_packages_not_inducted(self, client, session):
        """Test stowing packages that haven't been inducted"""
        warehouse = Warehouse(id="test_wh4", name="Test Warehouse 4")
        location = Location(id="loc1", warehouse=warehouse, zone="RECEIVING")

        package = Package(
            id="test_pkg_not_inducted",
            warehouse=warehouse,
            status=PackageStatus.PENDING,
            received_timestamp=None,
        )

        session.add_all([warehouse, location, package])
        session.flush()

        mutation = """
        mutation StowPackages($packageStow: PackageStowInput!) {
            stowPackages(packageStow: $packageStow) {
                success
                message
            }
        }
        """

        variables = {
            "packageStow": {
                "warehouseId": warehouse.id,
                "palletId": "test_pallet2",
                "packageIds": [package.id],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["stowPackages"]
        assert response["success"] is False
        assert "has not been inducted" in response["message"]

    def test_stow_packages_already_stowed(self, client, session):
        """Test stowing packages already stowed in another pallet"""
        from datetime import UTC, datetime

        warehouse = Warehouse(id="test_wh5", name="Test Warehouse 5")
        location = Location(id="rec_loc1", warehouse=warehouse, zone="RECEIVING")

        existing_pallet = Pallet(
            id="existing_pallet", warehouse=warehouse, location=location
        )
        package = Package(
            id="test_pkg_stowed",
            warehouse=warehouse,
            status=PackageStatus.STOWED,
            received_timestamp=datetime.now(UTC),
            pallet=existing_pallet,
        )

        session.add_all([warehouse, location, existing_pallet, package])
        session.flush()

        mutation = """
        mutation StowPackages($packageStow: PackageStowInput!) {
            stowPackages(packageStow: $packageStow) {
                success
                message
            }
        }
        """

        variables = {
            "packageStow": {
                "warehouseId": warehouse.id,
                "palletId": "new_pallet",
                "packageIds": [package.id],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["stowPackages"]
        assert response["success"] is False
        assert "already stowed in another pallet" in response["message"]

    def test_stow_packages_fails_given_pallet_not_in_receiving_zone(
        self, client, session
    ):
        """Test stowing packages already stowed in another pallet"""

        warehouse = Warehouse(id="test_wh5", name="Test Warehouse 5")
        location = Location(id="rec_loc1", warehouse=warehouse, zone="STORAGE")

        existing_pallet = Pallet(
            id="existing_pallet", warehouse=warehouse, location=location
        )
        package = Package(
            id="test_pkg_stowed", warehouse=warehouse, status=PackageStatus.INDUCTED
        )

        session.add_all([warehouse, location, existing_pallet, package])
        session.flush()

        mutation = """
        mutation StowPackages($packageStow: PackageStowInput!) {
            stowPackages(packageStow: $packageStow) {
                success
                message
            }
        }
        """

        variables = {
            "packageStow": {
                "warehouseId": warehouse.id,
                "palletId": existing_pallet.id,
                "packageIds": [package.id],
            }
        }

        response = client.post(
            "/graphql", json={"query": mutation, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result
        response = result["data"]["stowPackages"]
        assert response["success"] is False
        assert "is not in a receiving zone" in response["message"]
