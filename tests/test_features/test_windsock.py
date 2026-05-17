from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.features import Windsock


RAW_LINE = "19 41.2850 2.0750 1 Test Windsock"


class TestWindsock:
    def setup_method(self):
        self.windsock = Windsock.from_line(AptDatLine(RAW_LINE))

    def test_latitude(self):
        assert self.windsock.latitude == 41.285

    def test_longitude(self):
        assert self.windsock.longitude == 2.075

    def test_illuminated_true(self):
        assert self.windsock.illuminated is True
        assert isinstance(self.windsock.illuminated, bool)

    def test_illuminated_false(self):
        w = Windsock.from_line(AptDatLine("19 41.0 2.0 0 Dark Sock"))
        assert w.illuminated is False

    def test_name(self):
        assert self.windsock.name == "Test Windsock"

    def test_to_record_geometry_type(self):
        assert self.windsock._to_record()["geometry"]["type"] == "Point"

    def test_schema_geometry(self):
        assert Windsock._schema()["geometry"] == "Point"
