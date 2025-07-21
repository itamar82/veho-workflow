import pytest

from apps.db.entities import Location, Package, PackageStatus, Pallet, Warehouse


class TestQueryResolvers:
    """Integration tests for query resolvers"""

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        warehouse = Warehouse(id="wh1", name="test")
        session.add(warehouse)

        location = Location(id="loc1", warehouse=warehouse, zone="RECEIVING")
        session.add(location)

        packages = [
            Package(
                id=f"pkg_{i}",
                warehouse=warehouse,
                status=PackageStatus.PENDING,
                received_timestamp=None,
            )
            for i in range(10)
        ]

        session.add_all(packages)
        session.flush()

        pallet = Pallet(
            id="pallet_1",
            warehouse=warehouse,
            packages=packages[0:5],
            location=location,
        )
        session.add(pallet)
        session.flush()

    def test_get_packages_by_ids_success(self, client):
        """Test successful package retrieval by IDs"""
        query = """
        query GetPackages($warehouseId: String!, $packageIds: [String!]!) {
            getPackagesByIds(warehouseId: $warehouseId, packageIds: $packageIds) {
                id
                status
                warehouse {
                    id
                    name
                }
                receivedTimestamp
            }
        }
        """

        variables = {"warehouseId": "wh1", "packageIds": ["pkg_1", "pkg_2"]}

        response = client.post(
            "/graphql", json={"query": query, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result

        packages = result["data"]["getPackagesByIds"]
        assert len(packages) > 0

    def test_get_packages_by_ids_empty_result(self, client):
        """Test package retrieval with non-existent IDs"""
        query = """
        query GetPackages($warehouseId: String!, $packageIds: [String!]!) {
            getPackagesByIds(warehouseId: $warehouseId, packageIds: $packageIds) {
                id
                status
            }
        }
        """

        variables = {"warehouseId": "wh1", "packageIds": ["none", "none2"]}

        response = client.post(
            "/graphql", json={"query": query, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result

        packages = result["data"]["getPackagesByIds"]
        assert len(packages) == 0

    def test_get_pallets_by_ids_success(self, client):
        """Test successful pallet retrieval by IDs"""
        query = """
        query GetPallets($warehouseId: String!, $palletIds: [String!]!) {
            getPalletsByIds(warehouseId: $warehouseId, palletIds: $palletIds) {
                id
                warehouse {
                    id
                    name
                }
                packages {
                    id
                    status
                }
                location {
                    id
                    zone
                }
            }
        }
        """

        variables = {"warehouseId": "wh1", "palletIds": ["pallet_1"]}

        response = client.post(
            "/graphql", json={"query": query, "variables": variables}
        )
        assert response.status_code == 200

        result = response.json()
        assert "data" in result

        pallets = result["data"]["getPalletsByIds"]
        assert len(pallets) == 1
