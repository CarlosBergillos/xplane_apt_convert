from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.enums import LineLightingType, LineType
from xplane_apt_convert.features import LinearFeature
from xplane_apt_convert.iterators import BIterator


LINEAR_LINES = [
    "111 41.2800 2.0700 1 0",
    "115 41.2900 2.0800 1 0",
]


class TestLinearFeature:
    def setup_method(self):
        header = AptDatLine("120 Test Linear Feature")
        iterator = BIterator([AptDatLine(l) for l in LINEAR_LINES])
        features = LinearFeature.from_row_iterator(header, iterator, bezier_resolution=4)
        assert len(features) == 1
        self.feature = features[0]

    def test_name(self):
        assert self.feature.name == "Test Linear Feature"

    def test_has_coordinates(self):
        assert len(self.feature.coordinates) >= 2

    def test_painted_line_type(self):
        assert self.feature.painted_line_type == LineType.SOLID_YELLOW

    def test_lighting_line_type(self):
        assert self.feature.lighting_line_type == LineLightingType.NONE

    def test_to_record_geometry_type(self):
        assert self.feature._to_record()["geometry"]["type"] == "LineString"

    def test_to_record_properties(self):
        props = self.feature._to_record()["properties"]
        assert props["painted_line_type"] == "SOLID_YELLOW"
        assert props["name"] == "Test Linear Feature"

    def test_schema_geometry(self):
        assert LinearFeature._schema()["geometry"] == "LineString"
