from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.enums import SurfaceType
from xplane_apt_convert.features import Pavement
from xplane_apt_convert.iterators import BIterator


PAVEMENT_LINES = [
    "111 41.2800 2.0700 0 0",
    "111 41.2900 2.0700 0 0",
    "111 41.2900 2.0800 0 0",
    "113 41.2800 2.0800 0 0",
]


class TestPavement:
    def setup_method(self):
        header = AptDatLine("110 1 0.25 0.0 Test Pavement")
        iterator = BIterator([AptDatLine(l) for l in PAVEMENT_LINES])
        self.pavement = Pavement.from_row_iterator(header, iterator, bezier_resolution=4)

    def test_surface_type(self):
        assert self.pavement.surface_type == SurfaceType.ASPHALT

    def test_smoothness(self):
        assert self.pavement.smoothness == 0.25

    def test_texture_orientation(self):
        assert self.pavement.texture_orientation == 0.0

    def test_name(self):
        assert self.pavement.name == "Test Pavement"

    def test_has_one_ring(self):
        assert len(self.pavement.coordinates) == 1

    def test_ring_has_enough_points(self):
        assert len(self.pavement.coordinates[0]) >= 3

    def test_to_record_geometry_type(self):
        assert self.pavement._to_record()["geometry"]["type"] == "Polygon"

    def test_to_record_properties(self):
        props = self.pavement._to_record()["properties"]
        assert props["surface_type"] == "ASPHALT"
        assert props["smoothness"] == 0.25

    def test_schema_geometry(self):
        assert Pavement._schema()["geometry"] == "Polygon"
