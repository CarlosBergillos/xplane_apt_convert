from collections import OrderedDict
from dataclasses import dataclass

from xplane_airports import AptDat

from ..enums import LineLightingType, LineType
from ..geometry import get_paths
from ..iterators import BIterator
from ._base import AptFeature


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
