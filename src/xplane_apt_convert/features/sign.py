from collections import OrderedDict
from dataclasses import dataclass

from xplane_airports import AptDat

from ..enums import SignSize
from ._base import AptFeature


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
