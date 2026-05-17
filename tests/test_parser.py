import json
import pytest


class TestParsedAirportParsing:
    def test_id(self, parsed_airport):
        assert parsed_airport.id == "LEBL"

    def test_runways_count(self, parsed_airport):
        assert len(parsed_airport.runways) == 1

    def test_windsocks_count(self, parsed_airport):
        assert len(parsed_airport.windsocks) == 1

    def test_signs_count(self, parsed_airport):
        assert len(parsed_airport.signs) == 1

    def test_startup_locations_count(self, parsed_airport):
        assert len(parsed_airport.startup_locations) == 1

    def test_startup_location_enriched(self, parsed_airport):
        loc = parsed_airport.startup_locations[0]
        assert loc.width_code == "A"
        assert loc.operation_type == "airline_ops"
        assert loc.airline_codes == "AA BB"

    def test_boundary_parsed(self, parsed_airport):
        assert parsed_airport.boundary is not None
        assert parsed_airport.boundary.name == "Test Boundary"

    def test_pavements_count(self, parsed_airport):
        assert len(parsed_airport.pavements) == 1

    def test_linear_features_count(self, parsed_airport):
        assert len(parsed_airport.linear_features) == 1

    def test_metadata_parsed(self, parsed_airport):
        assert parsed_airport.metadata["datum_type"] == "AIRAC"


class TestParsedAirportExport:
    def test_export_geojson_creates_files(self, parsed_airport, tmp_path):
        out = tmp_path / "LEBL.geojson"
        parsed_airport.export(out, driver="GeoJSON", features=["runways", "windsocks"])
        assert (tmp_path / "LEBL.runways.geojson").exists()
        assert (tmp_path / "LEBL.windsocks.geojson").exists()

    def test_export_geojson_valid_json(self, parsed_airport, tmp_path):
        out = tmp_path / "LEBL.geojson"
        parsed_airport.export(out, driver="GeoJSON", features=["runways"])
        content = (tmp_path / "LEBL.runways.geojson").read_text()
        data = json.loads(content)
        assert data["type"] == "FeatureCollection"
        assert len(data["features"]) == 1

    def test_export_gpkg_single_file(self, parsed_airport, tmp_path):
        out = tmp_path / "LEBL.gpkg"
        parsed_airport.export(out, driver="GPKG", features=["runways", "windsocks"])
        assert out.exists()

    def test_export_feature_subset_only_creates_requested_files(self, parsed_airport, tmp_path):
        out = tmp_path / "LEBL.geojson"
        parsed_airport.export(out, driver="GeoJSON", features=["runways"])
        assert (tmp_path / "LEBL.runways.geojson").exists()
        assert not (tmp_path / "LEBL.windsocks.geojson").exists()

    def test_export_invalid_driver_raises(self, parsed_airport, tmp_path):
        with pytest.raises(ValueError, match="Invalid driver"):
            parsed_airport.export(tmp_path / "x.geojson", driver="BadDriver")

    def test_export_directory_path_raises(self, parsed_airport, tmp_path):
        with pytest.raises(ValueError, match="cannot be a directory"):
            parsed_airport.export("some/path/", driver="GeoJSON")

    def test_export_auto_detects_driver_from_extension(self, parsed_airport, tmp_path):
        out = tmp_path / "LEBL.geojson"
        parsed_airport.export(out, features=["runways"])
        assert (tmp_path / "LEBL.runways.geojson").exists()

    def test_export_unknown_extension_without_driver_raises(self, parsed_airport, tmp_path):
        with pytest.raises(ValueError):
            parsed_airport.export(tmp_path / "LEBL.xyz", features=["runways"])

    def test_export_crs_transform_changes_coordinates(self, parsed_airport, tmp_path):
        parsed_airport.export(tmp_path / "a.geojson", driver="GeoJSON", features=["runways"])
        parsed_airport.export(tmp_path / "b.geojson", driver="GeoJSON", features=["runways"], crs="EPSG:3857")
        coords_4326 = json.loads((tmp_path / "a.runways.geojson").read_text())["features"][0]["geometry"]["coordinates"][0]
        coords_3857 = json.loads((tmp_path / "b.runways.geojson").read_text())["features"][0]["geometry"]["coordinates"][0]
        assert coords_4326 != coords_3857
