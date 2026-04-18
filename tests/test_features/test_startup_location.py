from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.features import StartupLocation


RAW_1300 = "1300 41.2870 2.0770 90.0 gate props Gate 1"
RAW_1301_FULL = "1301 A airline_ops AA BB"
RAW_1301_SHORT = "1301 B"


class TestStartupLocation:
    def setup_method(self):
        self.loc = StartupLocation.from_line(AptDatLine(RAW_1300))

    def test_latitude(self):
        assert self.loc.latitude == 41.287

    def test_longitude(self):
        assert self.loc.longitude == 2.077

    def test_heading(self):
        assert self.loc.heading == 90.0

    def test_location_type(self):
        assert self.loc.location_type == "gate"

    def test_airplane_types(self):
        assert self.loc.airplane_types == "props"

    def test_name(self):
        assert self.loc.name == "Gate 1"

    def test_optional_fields_none_by_default(self):
        assert self.loc.width_code is None
        assert self.loc.operation_type is None
        assert self.loc.airline_codes is None

    def test_enrich_sets_all_fields(self):
        self.loc.enrich_from_metadata_line(AptDatLine(RAW_1301_FULL))
        assert self.loc.width_code == "A"
        assert self.loc.operation_type == "airline_ops"
        assert self.loc.airline_codes == "AA BB"

    def test_enrich_short_line_leaves_optionals_none(self):
        self.loc.enrich_from_metadata_line(AptDatLine(RAW_1301_SHORT))
        assert self.loc.width_code == "B"
        assert self.loc.operation_type is None
        assert self.loc.airline_codes is None

    def test_to_record_geometry_type(self):
        assert self.loc._to_record()["geometry"]["type"] == "Point"

    def test_schema_geometry(self):
        assert StartupLocation._schema()["geometry"] == "Point"
