from xplane_airports.AptDat import AptDatLine

from xplane_apt_convert.geometry import get_paths
from xplane_apt_convert.iterators import BIterator


def make_iter(lines):
    return BIterator([AptDatLine(l) for l in lines])


class TestGetPaths:
    def test_simple_line_two_points(self):
        it = make_iter(["111 41.28 2.07 1 0", "115 41.29 2.08 1 0"])
        coords, _ = get_paths(it, bezier_resolution=4, mode="line")
        assert len(coords) == 1
        assert coords[0][0] == (2.07, 41.28)
        assert coords[0][-1] == (2.08, 41.29)

    def test_simple_polygon_ring(self):
        it = make_iter([
            "111 41.28 2.07",
            "111 41.29 2.07",
            "111 41.29 2.08",
            "113 41.28 2.08",
        ])
        coords, _ = get_paths(it, bezier_resolution=4, mode="polygon")
        assert len(coords) == 1
        assert len(coords[0]) >= 3

    def test_line_captures_painted_type(self):
        it = make_iter(["111 41.28 2.07 3 0", "115 41.29 2.08 3 0"])
        _, props = get_paths(it, bezier_resolution=4, mode="line")
        assert props[0]["painted_line_type"] == 3

    def test_line_captures_lighting_type(self):
        it = make_iter(["111 41.28 2.07 1 101", "115 41.29 2.08 1 101"])
        _, props = get_paths(it, bezier_resolution=4, mode="line")
        assert props[0]["lighting_line_type"] == 101

    def test_empty_iterator_returns_empty(self):
        it = make_iter([])
        coords, props = get_paths(it, bezier_resolution=4, mode="line")
        assert coords == []
        assert props == []

    def test_coords_and_props_same_length(self):
        it = make_iter(["111 41.28 2.07 1 0", "115 41.29 2.08 1 0"])
        coords, props = get_paths(it, bezier_resolution=4, mode="line")
        assert len(coords) == len(props)

    def test_line_type_change_splits_segment(self):
        it = make_iter([
            "111 41.28 2.07 1 0",
            "111 41.29 2.08 2 0",  # different painted_line_type → new segment
            "115 41.30 2.09 2 0",
        ])
        coords, props = get_paths(it, bezier_resolution=4, mode="line")
        assert len(coords) == 2
        assert props[0]["painted_line_type"] == 1
        assert props[1]["painted_line_type"] == 2
