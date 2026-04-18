from collections import OrderedDict
from dataclasses import dataclass

from xplane_airports import AptDat

from ._base import AptFeature


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
