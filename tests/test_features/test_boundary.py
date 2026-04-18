from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.features import Boundary
from xplane_apt_convert.iterators import BIterator


BOUNDARY_LINES = [
    "111 41.2750 2.0650",
    "111 41.2950 2.0650",
    "111 41.2950 2.0850",
    "113 41.2750 2.0850",
]


class TestBoundary:
    def setup_method(self):
        header = AptDatLine("130 Test Boundary")
        iterator = BIterator([AptDatLine(l) for l in BOUNDARY_LINES])
        self.boundary = Boundary.from_row_iterator(header, iterator, bezier_resolution=4)

    def test_name(self):
        assert self.boundary.name == "Test Boundary"

    def test_has_one_ring(self):
        assert len(self.boundary.coordinates) == 1

    def test_ring_has_enough_points(self):
        assert len(self.boundary.coordinates[0]) >= 3

    def test_to_record_geometry_type(self):
        assert self.boundary._to_record()["geometry"]["type"] == "Polygon"

    def test_to_record_name_property(self):
        assert self.boundary._to_record()["properties"]["name"] == "Test Boundary"

    def test_schema_geometry(self):
        assert Boundary._schema()["geometry"] == "Polygon"
