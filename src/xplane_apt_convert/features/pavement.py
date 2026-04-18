from collections import OrderedDict
from dataclasses import dataclass

from xplane_airports import AptDat

from ..enums import SurfaceType
from ..geometry import get_paths
from ..iterators import BIterator
from ._base import AptFeature


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
