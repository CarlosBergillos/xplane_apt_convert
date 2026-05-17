from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.features.metadata import AptMetadata


class TestAptMetadata:
    def test_add_from_row_stores_key_value(self):
        meta = AptMetadata()
        meta.add_from_row(AptDatLine("1302 datum_type nav_data"))
        assert meta["datum_type"] == "nav_data"

    def test_add_from_row_no_value_stores_none(self):
        meta = AptMetadata()
        meta.add_from_row(AptDatLine("1302 some_key"))
        assert meta["some_key"] is None

    def test_multiple_rows(self):
        meta = AptMetadata()
        meta.add_from_row(AptDatLine("1302 key1 val1"))
        meta.add_from_row(AptDatLine("1302 key2 val2"))
        assert meta["key1"] == "val1"
        assert meta["key2"] == "val2"

    def test_is_dict(self):
        assert isinstance(AptMetadata(), dict)
