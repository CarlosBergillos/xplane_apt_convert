import pytest

from xplane_apt_convert.enums import (
    FallbackEnum,
    LineLightingType,
    LineType,
    ApproachLighting,
    RunwayEndIdentifierLights,
    RunwayMarking,
    ShoulderSurfaceType,
    SignSize,
    SurfaceType,
)
from xplane_apt_convert.enums._fallback import FallbackEnumMeta


class TestFallbackEnum:
    def test_known_value_returns_member(self):
        assert SurfaceType(1) == SurfaceType.ASPHALT

    def test_unknown_value_returns_fallback_without_raising(self):
        result = SurfaceType(9999)
        assert isinstance(result, FallbackEnumMeta.Fallback)

    def test_unknown_value_fallback_name(self):
        result = SurfaceType(9999)
        assert result.name == "UNKNOWN_9999"

    def test_none_value_returns_fallback_with_none_name(self):
        result = SurfaceType(None)
        assert isinstance(result, FallbackEnumMeta.Fallback)
        assert result.name is None

    def test_unknown_value_deduplicated_in_logged_unknowns(self):
        from xplane_apt_convert.enums._fallback import logged_unknowns
        logged_unknowns.clear()
        SurfaceType(7777)
        SurfaceType(7777)
        count = sum(1 for (cls, val) in logged_unknowns if val == 7777)
        assert count == 1


class TestSurfaceType:
    def test_asphalt(self):
        assert SurfaceType(1).name == "ASPHALT"

    def test_concrete(self):
        assert SurfaceType(2).name == "CONCRETE"

    def test_water_runway(self):
        assert SurfaceType(13).name == "WATER_RUNWAY"


class TestShoulderSurfaceType:
    def test_none(self):
        assert ShoulderSurfaceType(0).name == "NONE"

    def test_asphalt(self):
        assert ShoulderSurfaceType(1).name == "ASPHALT"


class TestLineType:
    def test_none(self):
        assert LineType(0).name == "NONE"

    def test_solid_yellow(self):
        assert LineType(1).name == "SOLID_YELLOW"

    def test_solid_white(self):
        assert LineType(20).name == "SOLID_WHITE"


class TestLineLightingType:
    def test_none(self):
        assert LineLightingType(0).name == "NONE"

    def test_green_bidirectional(self):
        assert LineLightingType(101).name == "GREEN_BIDIRECTIONAL_LIGHTS"


class TestRunwayMarking:
    def test_none(self):
        assert RunwayMarking(0).name == "NONE"

    def test_precision(self):
        assert RunwayMarking(3).name == "PRECISION"


class TestApproachLighting:
    def test_none(self):
        assert ApproachLighting(0).name == "NONE"

    def test_alsf_i(self):
        assert ApproachLighting(1).name == "ALSF_I"


class TestRunwayEndIdentifierLights:
    def test_none(self):
        assert RunwayEndIdentifierLights(0).name == "NONE"

    def test_omnidirectional(self):
        assert RunwayEndIdentifierLights(1).name == "OMNIDIRECTIONAL_REIL"


class TestSignSize:
    def test_small(self):
        assert SignSize(1).name == "SMALL"

    def test_large_distance_remaining(self):
        assert SignSize(4).name == "LARGE_DISTANCE_REMAINING"
