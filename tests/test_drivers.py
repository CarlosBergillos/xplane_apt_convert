from pathlib import Path

from xplane_apt_convert.drivers import (
    SUPPORTED_DRIVERS,
    VALID_FEATURES,
    _detect_driver,
)


class TestDetectDriver:
    def test_geojson(self):
        assert _detect_driver(Path("x.geojson")) == "GeoJSON"

    def test_json(self):
        assert _detect_driver(Path("x.json")) == "GeoJSON"

    def test_gpkg(self):
        assert _detect_driver(Path("x.gpkg")) == "GPKG"

    def test_shp(self):
        assert _detect_driver(Path("x.shp")) == "ESRI Shapefile"

    def test_fgb(self):
        assert _detect_driver(Path("x.fgb")) == "FlatGeobuf"

    def test_geojsonl(self):
        assert _detect_driver(Path("x.geojsonl")) == "GeoJSONSeq"

    def test_sqlite(self):
        assert _detect_driver(Path("x.sqlite")) == "SQLite"

    def test_gml(self):
        assert _detect_driver(Path("x.gml")) == "GML"

    def test_gmt(self):
        assert _detect_driver(Path("x.gmt")) == "OGR_GMT"

    def test_unknown_extension_returns_none(self):
        assert _detect_driver(Path("x.xyz")) is None

    def test_no_extension_returns_none(self):
        assert _detect_driver(Path("noextension")) is None

    def test_case_insensitive(self):
        assert _detect_driver(Path("x.GEOJSON")) == "GeoJSON"


class TestSupportedDrivers:
    def test_all_eight_drivers_present(self):
        expected = {
            "ESRI Shapefile", "FlatGeobuf", "GeoJSON", "GeoJSONSeq",
            "GPKG", "GML", "OGR_GMT", "SQLite",
        }
        assert set(SUPPORTED_DRIVERS.keys()) == expected

    def test_multilayer_drivers(self):
        assert SUPPORTED_DRIVERS["GPKG"]["multilayer"] is True
        assert SUPPORTED_DRIVERS["SQLite"]["multilayer"] is True

    def test_single_layer_drivers(self):
        assert SUPPORTED_DRIVERS["GeoJSON"]["multilayer"] is False
        assert SUPPORTED_DRIVERS["ESRI Shapefile"]["multilayer"] is False

    def test_each_driver_has_required_keys(self):
        for driver, info in SUPPORTED_DRIVERS.items():
            assert "multilayer" in info, driver
            assert "extensions" in info, driver
            assert "default_extension" in info, driver


class TestValidFeatures:
    def test_count(self):
        assert len(VALID_FEATURES) == 7

    def test_contains_expected(self):
        for name in ["boundary", "runways", "startup_locations", "windsocks",
                     "signs", "pavements", "linear_features"]:
            assert name in VALID_FEATURES
