from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.enums import SignSize
from xplane_apt_convert.features import Sign


RAW_LINE = "20 41.2860 2.0760 180.0 0 1 {A-1}"


class TestSign:
    def setup_method(self):
        self.sign = Sign.from_line(AptDatLine(RAW_LINE))

    def test_latitude(self):
        assert self.sign.latitude == 41.286

    def test_longitude(self):
        assert self.sign.longitude == 2.076

    def test_heading(self):
        assert self.sign.heading == 180.0

    def test_size(self):
        assert self.sign.size == SignSize.SMALL

    def test_text(self):
        assert self.sign.text == "{A-1}"

    def test_to_record_geometry_type(self):
        assert self.sign._to_record()["geometry"]["type"] == "Point"

    def test_to_record_coordinate_order(self):
        coords = self.sign._to_record()["geometry"]["coordinates"]
        assert coords == (2.076, 41.286)

    def test_schema_geometry(self):
        assert Sign._schema()["geometry"] == "Point"
