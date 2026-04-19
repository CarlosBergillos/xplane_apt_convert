from collections import OrderedDict
from dataclasses import dataclass

from xplane_airports import AptDat

from ..geometry import get_paths
from ..iterators import BIterator
from ._base import AptFeature


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
