from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.enums import SurfaceType
from xplane_apt_convert.features import Runway


RAW_LINE = "100 45.00 1 0 0.25 1 3 1 09L 41.2800 2.0700 0 0 0 0 0 0 27R 41.2900 2.0900 0 0 0 0 0 0"


class TestRunway:
    def setup_method(self):
        self.runway = Runway.from_line(AptDatLine(RAW_LINE))

    def test_width(self):
        assert self.runway.width == 45.0

    def test_surface_type(self):
        assert self.runway.surface_type == SurfaceType.ASPHALT

    def test_end_names(self):
        assert self.runway.ends[0].name == "09L"
        assert self.runway.ends[1].name == "27R"

    def test_end_coordinates(self):
        assert self.runway.ends[0].latitude == 41.28
        assert self.runway.ends[0].longitude == 2.07

    def test_to_record_geometry_type(self):
        record = self.runway._to_record()
        assert record["geometry"]["type"] == "LineString"

    def test_to_record_has_two_coordinates(self):
        coords = self.runway._to_record()["geometry"]["coordinates"]
        assert len(coords) == 2

    def test_to_record_coordinate_order(self):
        coords = self.runway._to_record()["geometry"]["coordinates"]
        # GeoJSON is (lon, lat)
        assert coords[0] == (2.07, 41.28)
        assert coords[1] == (2.09, 41.29)

    def test_schema_geometry(self):
        assert Runway._schema()["geometry"] == "LineString"

    def test_schema_has_surface_type_property(self):
        assert "surface_type" in Runway._schema()["properties"]
