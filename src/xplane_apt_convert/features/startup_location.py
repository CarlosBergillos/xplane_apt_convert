from collections import OrderedDict
from dataclasses import dataclass
from typing import Optional

from xplane_airports import AptDat

from ._base import AptFeature


@dataclass
class StartupLocation(AptFeature):
    latitude: float
    longitude: float
    heading: float
    location_type: str
    airplane_types: str
    name: str
    width_code: Optional[str] = None
    operation_type: Optional[str] = None
    airline_codes: Optional[str] = None

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

    def enrich_from_metadata_line(self, line: AptDat.AptDatLine) -> None:
        tokens = line.tokens
        self.width_code = tokens[1] if len(tokens) > 1 else None
        self.operation_type = tokens[2] if len(tokens) > 2 else None
        self.airline_codes = " ".join(tokens[3:]) if len(tokens) > 3 else None

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
                    ("width_code", "str"),
                    ("operation_type", "str"),
                    ("airline_codes", "str"),
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
                "width_code": self.width_code,
                "operation_type": self.operation_type,
                "airline_codes": self.airline_codes,
            },
        }
