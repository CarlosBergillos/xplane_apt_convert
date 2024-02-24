from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum, EnumMeta
import logging

from .geometry import get_paths
from .iterators import BIterator

try:
    from xplane_airports import AptDat
except ImportError as e:
    raise ImportError(
        "Could not import xplane_airports. "
        "Install https://github.com/X-Plane/xplane_airports."
    ) from e


logger = logging.getLogger("xplane_apt_convert")

# TODO: this should be reset with each different airport parsing
logged_unknowns = set()


class FallbackEnumMeta(EnumMeta):
    class Fallback:
        def __init__(self, name):
            self.name = name

    def __call__(cls, value, names=None, *args, **kwargs):
        try:
            return EnumMeta.__call__(cls, value, names=None, *args, **kwargs)
        except ValueError:
            if names is not None:
                # using functional API attempting to create a new Enum type
                raise

            if value is None:
                return FallbackEnumMeta.Fallback(None)
            else:
                if (cls, value) not in logged_unknowns:
                    logger.warning(f"Unknown value {value} found for {cls.__name__}.")
                    # do not log same warning many times
                    logged_unknowns.add((cls, value))

                return FallbackEnumMeta.Fallback(f"UNKNOWN_{value}")


class FallbackEnum(Enum, metaclass=FallbackEnumMeta):
    """Custom subclass of Enum that supports handling of arbitrary unknown values."""


class LineType(FallbackEnum):
    NONE = 0
    SOLID_YELLOW = 1
    BROKEN_YELLOW = 2
    DOUBLE_SOLID_YELLOW = 3
    RUNWAY_HOLD = 4  # DOUBLE_BROKEN_YELLOW_WITH_PARALLEL_DOUBLE_SOLID_YELLOW = 4
    OTHER_HOLD = 5  # BROKEN_YELLOW_WITH_PARALLEL_SOLID_YELLOW = 5
    ILS_HOLD = 6  # YELLOW_CROSSHATCHED = 6
    ILS_CRITICAL_CENTERLINE = 7
    SEPARATED_BROKEN_YELLOW = 8
    SEPARATED_DOUBLE_BROKEN_YELLOW = 9
    WIDE_SOLID_YELLOW = 10
    WIDE_ILS_CRITICAL_CENTERLINE = 11
    WIDE_RUNWAY_HOLD = 12
    WIDE_OTHER_HOLD = 13
    WIDE_ILS_HOLD = 14

    SOLID_YELLOW_WITH_BLACK_BORDER = 51
    BROKEN_YELLOW_WITH_BLACK_BORDER = 52
    DOUBLE_SOLID_YELLOW_WITH_BLACK_BORDER = 53
    RUNWAY_HOLD_WITH_BLACK_BORDER = 54
    OTHER_HOLD_WITH_BLACK_BORDER = 55
    ILS_HOLD_WITH_BLACK_BORDER = 56
    ILS_CRITICAL_CENTERLINE_WITH_BLACK_BORDER = 57
    SEPARATED_BROKEN_YELLOW_WITH_BLACK_BORDER = 58
    SEPARATED_DOUBLE_BROKEN_YELLOW_WITH_BLACK_BORDER = 59
    WIDE_SOLID_YELLOW_WITH_BLACK_BORDER = 60
    WIDE_ILS_CRITICAL_CENTERLINE_WITH_BLACK_BORDER = 61
    WIDE_RUNWAY_HOLD_WITH_BLACK_BORDER = 62
    WIDE_OTHER_HOLD_WITH_BLACK_BORDER = 63
    WIDE_ILS_HOLD_WITH_BLACK_BORDER = 64

    VERY_WIDE_YELLOW = 19

    SOLID_WHITE = 20
    CHEQUERED_WHITE = 21
    BROKEN_WHITE = 22
    SHORT_BROKEN_WHITE = 23
    WIDE_SOLID_WHITE = 24
    WIDE_BROKEN_WHITE = 25
    SOLID_RED = 30
    BROKEN_RED = 31
    WIDE_SOLID_RED = 32
    SOLID_ORANGE = 40
    SOLID_BLUE = 41
    SOLID_GREEN = 42

    SOLID_WHITE_WITH_BLACK_BORDER = 70
    CHEQUERED_WHITE_WITH_BLACK_BORDER = 71
    BROKEN_WHITE_WITH_BLACK_BORDER = 72
    SHORT_BROKEN_WHITE_WITH_BLACK_BORDER = 73
    WIDE_SOLID_WHITE_WITH_BLACK_BORDER = 74
    WIDE_BROKEN_WHITE_WITH_BLACK_BORDER = 75
    SOLID_RED_WITH_BLACK_BORDER = 80
    BROKEN_RED_WITH_BLACK_BORDER = 81
    WIDE_SOLID_RED_WITH_BLACK_BORDER = 82
    SOLID_ORANGE_WITH_BLACK_BORDER = 90
    SOLID_BLUE_WITH_BLACK_BORDER = 91
    SOLID_GREEN_WITH_BLACK_BORDER = 92


class LineLightingType(FallbackEnum):
    NONE = 0
    GREEN_BIDIRECTIONAL_LIGHTS = 101
    BLUE_OMNIDIRECTIONAL_LIGHTS = 102
    AMBER_UNIDIRECTIONAL_LIGHTS = 103
    AMBER_UNIDIRECTIONAL_PULSATING_LIGHTS = 104
    ALTERNATING_AMBER_GREEN_BIDIRECTIONAL_LIGHTS = 105
    RED_OMNIDIRECTIONAL_LIGHTS = 106
    GREEN_UNIDIRECTIONAL_LIGHTS = 107
    ALTERNATING_AMBER_GREEN_UNIDIRECTIONAL_LIGHTS = 108


class SurfaceType(FallbackEnum):
    ASPHALT = 1  # Asphalt
    CONCRETE = 2  # Concrete
    TURF_OR_GRASS = 3  # Turf or grass
    DIRT = 4  # Dirt (brown)
    GRAVEL = 5  # Gravel (grey)
    DRY_LAKEBED = 12  # Dry lakebed
    WATER_RUNWAY = 13  # Water runway
    SNOW_OR_ICE = 14  # Snow or ice
    TRANSPARENT = 15  # Transparent


class ShoulderSurfaceType(FallbackEnum):
    NONE = 0  # No shoulder
    ASPHALT = 1  # Asphalt shoulder
    CONCRETE = 2  # Concrete shoulder


class RunwayMarking(FallbackEnum):
    NONE = 0  # No runway markings
    VISUAL = 1  # Visual markings
    NON_PRECISION = 2  # Non-precision approach markings
    PRECISION = 3  # Precision approach markings
    UK_NON_PRECISION = 4  # UK-style non-precision approach markings
    UK_PRECISION = 5  # UK-style precision approach markings


class ApproachLighting(FallbackEnum):
    NONE = 0  # No approach lighting
    ALSF_I = 1  # ALSF-I. Approach Lighting System with Sequenced Flashing Lights
    ALSF_II = 2  # ALSF-II. Approach Lighting System with Sequenced Flashing Lights
    CALVERT = 3  # Calvert
    CALVERT_II = 4  # Calvert ILS Cat II and Cat II
    SSALR = 5  # SSALR. Simplified Short Approach Lighting System with Runway Alignment Indicator Lights
    SSALF = 6  # SSALF. Simplified Short Approach Lighting System with Sequenced Flashing Lights
    SALS = 7  # SALS. Short Approach Light System
    MALSR = 8  # MALSR. Medium-intensity Approach Light System with Runway Alignment Indicator Lights
    MALSF = 9  # MALSF. Medium-intensity Approach Light System with Sequenced Flashing Lights
    MALS = 10  # MALS. Medium-intensity Approach Light System
    ODALS = 11  # ODALS. Omni-Directional Approach Light System
    RAIL = 12  # RAIL. Runway Alignment Indicator Lights


class RunwayEndIdentifierLights(FallbackEnum):
    NONE = 0  # No REIL
    OMNIDIRECTIONAL_REIL = 1  # Omni-directional REIL
    UNIDIRECTIONAL_REIL = 2  # Unidirectional REIL


class SignSize(FallbackEnum):
    SMALL = 1  # Small taxiway sign
    MEDIUM = 2  # Medium taxiway sign
    LARGE = 3  # Large taxiway sign
    LARGE_DISTANCE_REMAINING = 4  # Large distance-remaining sign on runway edge
    SMALL_DISTANCE_REMAINING = 5  # Small distance-remaining sign on runway edg


class AptMetadata(dict):
    def add_from_row(self, row: AptDat.AptDatLine):
        tokens = row.tokens

        key = tokens[1]
        value = tokens[2] if len(tokens) > 2 else None

        self[key] = value


class AptFeature(ABC):
    @staticmethod
    @abstractmethod
    def _schema() -> dict:
        pass

    @abstractmethod
    def _to_record(self) -> dict:
        pass


@dataclass
class Boundary(AptFeature):
    name: str
    coordinates: list[tuple[float, float]]

    @staticmethod
    def from_row_iterator(
        header_row: AptDat.AptDatLine, line_iterator: BIterator, bezier_resolution: int
    ) -> "Boundary":
        tokens = header_row.tokens
        coordinates_list, properties_list = get_paths(
            line_iterator,
            bezier_resolution=bezier_resolution,
            mode="polygon",
        )

        coordinates_list = [c for c in coordinates_list if len(c) > 2]
        properties_list = [
            p for c, p in zip(coordinates_list, properties_list) if len(c) > 2
        ]

        return Boundary(
            name=" ".join(tokens[1:]),
            coordinates=coordinates_list,
        )

    @staticmethod
    def _schema():
        return {
            "geometry": "Polygon",
            "properties": OrderedDict(
                [
                    ("name", "str"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "Polygon",
                "coordinates": self.coordinates,
            },
            "properties": {"name": self.name},
        }


@dataclass
class Pavement(AptFeature):
    surface_type: SurfaceType
    smoothness: float
    texture_orientation: float
    name: str
    coordinates: list[tuple[float, float]]

    @staticmethod
    def from_row_iterator(
        header_row: AptDat.AptDatLine, line_iterator: BIterator, bezier_resolution: int
    ) -> "Pavement":
        tokens = header_row.tokens
        coordinates_list, properties_list = get_paths(
            line_iterator,
            bezier_resolution=bezier_resolution,
            mode="polygon",
        )

        coordinates_list = [c for c in coordinates_list if len(c) > 2]
        properties_list = [
            p for c, p in zip(coordinates_list, properties_list) if len(c) > 2
        ]

        return Pavement(
            surface_type=SurfaceType(int(tokens[1])),
            smoothness=float(tokens[2]),
            texture_orientation=float(tokens[3]),
            name=" ".join(tokens[4:]),
            coordinates=coordinates_list,
        )

    @staticmethod
    def _schema():
        return {
            "geometry": "Polygon",
            "properties": OrderedDict(
                [
                    ("name", "str"),
                    ("surface_type", "str"),
                    ("smoothness", "float"),
                    ("texture_orientation", "float"),
                    # TODO: pavements can have edge lines,
                    # but they can cover only a segment of the edge,
                    # and/or have multiple types in different parts,
                    # so this can't be a pavement property.
                    # Probably consider making separate line features.
                    # ("painted_line_type", "int"),
                    # ("lighting_line_type", "int"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "Polygon",
                "coordinates": self.coordinates,
            },
            "properties": {
                "name": self.name,
                "surface_type": self.surface_type.name,
                "smoothness": self.smoothness,
                "texture_orientation": self.texture_orientation,
            },
        }


@dataclass
class LinearFeature(AptFeature):
    name: str
    painted_line_type: int
    lighting_line_type: int
    coordinates: list[tuple[float, float]]

    @staticmethod
    def from_row_iterator(
        header_row: AptDat.AptDatLine,
        line_iterator: BIterator,
        bezier_resolution: int,
    ) -> list["LinearFeature"]:
        tokens = header_row.tokens
        coordinates_list, properties_list = get_paths(
            line_iterator,
            bezier_resolution=bezier_resolution,
            mode="line",
        )

        return [
            LinearFeature(
                name=" ".join(tokens[1:]),
                painted_line_type=LineType(properties.get("painted_line_type")),
                lighting_line_type=LineLightingType(
                    properties.get("lighting_line_type")
                ),
                coordinates=coordinates,
            )
            for coordinates, properties in zip(coordinates_list, properties_list)
            if len(coordinates) > 1
        ]

    @staticmethod
    def _schema():
        return {
            "geometry": "LineString",
            "properties": OrderedDict(
                [
                    ("name", "str"),
                    ("painted_line_type", "str"),
                    ("lighting_line_type", "str"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "LineString",
                "coordinates": self.coordinates,
            },
            "properties": {
                "name": self.name,
                "painted_line_type": self.painted_line_type.name,
                "lighting_line_type": self.lighting_line_type.name,
            },
        }


@dataclass
class RunwayEnd:
    name: str
    latitude: float
    longitude: float
    dthr_length: float  # Displaced Threshold length in meters
    overrun_length: float  # in meters
    marking: RunwayMarking
    lighting: ApproachLighting
    tdz_lighting: bool  # Touchdown Zone lighting
    reil: int  # Runway End Identifier Lights

    @staticmethod
    def from_line_tokens(tokens: list[str]) -> "RunwayEnd":
        return RunwayEnd(
            name=tokens[0],
            latitude=float(tokens[1]),
            longitude=float(tokens[2]),
            dthr_length=float(tokens[3]),
            overrun_length=float(tokens[4]),
            marking=RunwayMarking(int(tokens[5])),
            lighting=ApproachLighting(int(tokens[6])),
            tdz_lighting=bool(int(tokens[7])),
            reil=RunwayEndIdentifierLights(int(tokens[8])),
        )


@dataclass
class Runway(AptFeature):
    width: float  # in meters
    surface_type: SurfaceType
    shoulder_surface_type: ShoulderSurfaceType
    smoothness: float
    centerline_lights: int
    edge_lights: int
    auto_distance_remaining_signs: bool
    ends: tuple[RunwayEnd, RunwayEnd]

    @staticmethod
    def from_line(line: AptDat.AptDatLine) -> "Runway":
        tokens = line.tokens
        return Runway(
            width=float(tokens[1]),
            surface_type=SurfaceType(int(tokens[2])),
            shoulder_surface_type=ShoulderSurfaceType(int(tokens[3])),
            smoothness=float(tokens[4]),
            centerline_lights=int(tokens[5]),
            edge_lights=int(tokens[6]),
            auto_distance_remaining_signs=bool(int(tokens[7])),
            ends=(
                RunwayEnd.from_line_tokens(tokens[8:17]),
                RunwayEnd.from_line_tokens(tokens[17:26]),
            ),
        )

    @staticmethod
    def _schema():
        return {
            "geometry": "LineString",
            "properties": OrderedDict(
                [
                    ("width", "float"),
                    ("surface_type", "str"),
                    ("shoulder_surface_type", "str"),
                    ("smoothness", "float"),
                    ("centerline_lights", "int"),
                    ("edge_lights", "int"),
                    ("auto_distance_remaining_signs", "bool"),
                    ("name_1", "str"),
                    ("name_2", "str"),
                    ("dthr_length_1", "float"),
                    ("dthr_length_2", "float"),
                    ("overrun_length_1", "float"),
                    ("overrun_length_2", "float"),
                    ("marking_1", "str"),
                    ("marking_2", "str"),
                    ("lighting_1", "str"),
                    ("lighting_2", "str"),
                    ("tdz_lighting_1", "bool"),
                    ("tdz_lighting_2", "bool"),
                    ("reil_1", "str"),
                    ("reil_2", "str"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    (self.ends[0].longitude, self.ends[0].latitude),
                    (self.ends[1].longitude, self.ends[1].latitude),
                ],
            },
            "properties": {
                "width": self.width,
                "surface_type": self.surface_type.name,
                "shoulder_surface_type": self.shoulder_surface_type.name,
                "smoothness": self.smoothness,
                "centerline_lights": self.centerline_lights,
                "edge_lights": self.edge_lights,
                "auto_distance_remaining_signs": self.auto_distance_remaining_signs,
                "name_1": self.ends[0].name,
                "name_2": self.ends[1].name,
                "dthr_length_1": self.ends[0].dthr_length,
                "dthr_length_2": self.ends[1].dthr_length,
                "overrun_length_1": self.ends[0].overrun_length,
                "overrun_length_2": self.ends[1].overrun_length,
                "marking_1": self.ends[0].marking.name,
                "marking_2": self.ends[1].marking.name,
                "lighting_1": self.ends[0].lighting.name,
                "lighting_2": self.ends[1].lighting.name,
                "tdz_lighting_1": self.ends[0].tdz_lighting,
                "tdz_lighting_2": self.ends[1].tdz_lighting,
                "reil_1": self.ends[0].reil.name,
                "reil_2": self.ends[1].reil.name,
            },
        }


@dataclass
class StartupLocation(AptFeature):
    latitude: float
    longitude: float
    heading: float
    location_type: str
    airplane_types: str
    name: str

    @staticmethod
    def from_line(line: AptDat.AptDatLine) -> "StartupLocation":
        tokens = line.tokens
        return StartupLocation(
            latitude=float(tokens[1]),
            longitude=float(tokens[2]),
            heading=float(tokens[3]),
            location_type=tokens[4],
            airplane_types=tokens[5],
            name=" ".join(tokens[6:]),
        )

    @staticmethod
    def _schema():
        return {
            "geometry": "Point",
            "properties": OrderedDict(
                [
                    ("heading", "float"),
                    ("location_type", "str"),
                    ("airplane_types", "str"),
                    ("name", "str"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": (self.longitude, self.latitude),
            },
            "properties": {
                "heading": self.heading,
                "location_type": self.location_type,
                "airplane_types": self.airplane_types,
                "name": self.name,
            },
        }


@dataclass
class Windsock(AptFeature):
    latitude: float
    longitude: float
    illuminated: bool
    name: str

    @staticmethod
    def from_line(line: AptDat.AptDatLine) -> "Windsock":
        tokens = line.tokens
        return Windsock(
            latitude=float(tokens[1]),
            longitude=float(tokens[2]),
            illuminated=bool(int(tokens[3])),
            name=" ".join(tokens[4:]),
        )

    @staticmethod
    def _schema():
        return {
            "geometry": "Point",
            "properties": OrderedDict(
                [
                    ("illuminated", "bool"),
                    ("name", "str"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": (self.longitude, self.latitude),
            },
            "properties": {
                "illuminated": self.illuminated,
                "name": self.name,
            },
        }


@dataclass
class Sign(AptFeature):
    latitude: float
    longitude: float
    heading: float
    size: SignSize
    text: str

    @staticmethod
    def from_line(line: AptDat.AptDatLine) -> "Sign":
        tokens = line.tokens
        return Sign(
            latitude=float(tokens[1]),
            longitude=float(tokens[2]),
            heading=float(tokens[3]),
            size=SignSize(int(tokens[5])),
            text=tokens[6],
        )

    @staticmethod
    def _schema():
        return {
            "geometry": "Point",
            "properties": OrderedDict(
                [
                    ("heading", "float"),
                    ("size", "str"),
                    ("text", "str"),
                ]
            ),
        }

    def _to_record(self):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": (self.longitude, self.latitude),
            },
            "properties": {
                "heading": self.heading,
                "size": self.size.name,
                "text": self.text,
            },
        }
