from collections import OrderedDict
from dataclasses import dataclass

from xplane_airports import AptDat

from ..enums import (
    ApproachLighting,
    RunwayEndIdentifierLights,
    RunwayMarking,
    ShoulderSurfaceType,
    SurfaceType,
)
from ._base import AptFeature


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
