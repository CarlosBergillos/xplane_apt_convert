from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Union, get_args, get_origin, get_type_hints

import fiona
from fiona.transform import transform_geom
from rich.logging import RichHandler

from .classes import (
    AptFeature,
    AptMetadata,
    Boundary,
    LinearFeature,
    Pavement,
    Runway,
    Sign,
    StartupLocation,
    Windsock,
)
from .geometry import _DEFAULT_BEZIER_RESOLUTION
from .iterators import BIterator

try:
    from xplane_airports import AptDat
except ImportError as e:
    raise ImportError(
        "Could not import xplane_airports. Install https://github.com/X-Plane/xplane_airports."
    ) from e


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(show_path=False, omit_repeated_times=False)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


_BASE_CRS = "EPSG:4326"

SUPPORTED_DRIVERS = {
    "ESRI Shapefile": {
        "multilayer": False,
        "extensions": ["shp", "dbf", "shz", "shp.zip"],
        "default_extension": "shp",
    },
    "FlatGeobuf": {
        "multilayer": False,
        "extensions": ["fgb"],
        "default_extension": "fgb",
    },
    "GeoJSON": {
        "multilayer": False,
        "extensions": ["json", "geojson"],
        "default_extension": "geojson",
    },
    "GeoJSONSeq": {
        "multilayer": False,
        "extensions": ["geojsonl", "geojsons"],
        "default_extension": "geojsonl",
    },
    "GPKG": {
        "multilayer": True,
        "extensions": ["gpkg"],
        "default_extension": "gpkg",
    },
    "GML": {
        "multilayer": False,
        "extensions": ["gml", "xml"],
        "default_extension": "gml",
    },
    "OGR_GMT": {
        "multilayer": False,
        "extensions": ["gmt"],
        "default_extension": "gmt",
    },
    "SQLite": {
        "multilayer": True,
        "extensions": ["sqlite", "db"],
        "default_extension": "sqlite",
    },
}


def _detect_driver(path: Path):
    """
    Attempt to auto-detect driver based on the extension
    """
    extension = path.suffix.lower().removeprefix(".")

    if not extension:
        return None

    for driver, driver_info in SUPPORTED_DRIVERS.items():
        driver_extensions = driver_info["extensions"]

        if extension in driver_extensions:
            return driver

    return None


VALID_FEATURES = [
    "boundary",
    "runways",
    "startup_locations",
    "windsocks",
    "signs",
    "pavements",
    "linear_features",
]


class ParsedAirport:
    id: str
    metadata: AptMetadata
    boundary: Optional[Boundary]
    runways: list[Runway]
    startup_locations: list[StartupLocation]
    signs: list[Sign]
    windsocks: list[Windsock]
    linear_features: list[LinearFeature]
    pavements: list[Pavement]

    def __init__(
        self,
        airport: AptDat.Airport,
        bezier_resolution: int = _DEFAULT_BEZIER_RESOLUTION,
    ) -> None:
        """A parsed X-Plane airport.

        Args:
            airport (xplane_airports.AptDat.Airport): An X-Plane airport object
                as obtained from `xplane_airports` (https://github.com/X-Plane/xplane_airports).
            bezier_resolution (int): Number of points to use to plot Bezier curves.
                A higher number means more resolution but also larger file sizes on export.
                Default 16.
        """
        self._airport = airport
        self.id = None
        self.metadata = AptMetadata()
        self.boundary = None
        self.runways = []
        self.startup_locations = []
        self.signs = []
        self.windsocks = []
        self.linear_features = []
        self.pavements = []

        self._parse(bezier_resolution=bezier_resolution)

    def _parse(self, bezier_resolution: int) -> None:
        logger.info("Parsing airport.")
        row_iterator = BIterator(self._airport.text)

        for row in row_iterator:
            row_code = row.row_code

            if row_code == AptDat.RowCode.AIRPORT_HEADER:
                self.id = row.tokens[4]

            if row_code == AptDat.RowCode.METADATA:
                self.metadata.add_from_row(row)

            elif row_code == AptDat.RowCode.BOUNDARY:
                logger.debug("Parsing boundary row.")

                boundary = Boundary.from_row_iterator(
                    row, row_iterator, bezier_resolution
                )

                if boundary is not None:
                    self.boundary = boundary

            elif row_code == AptDat.RowCode.LAND_RUNWAY:
                logger.debug("Parsing runway row.")

                runway = Runway.from_line(row)

                if runway is not None:
                    self.runways.append(runway)

            elif row_code == AptDat.RowCode.START_LOCATION_NEW:
                logger.debug("Parsing startup location row.")

                startup_location = StartupLocation.from_line(row)

                if startup_location is not None:
                    self.startup_locations.append(startup_location)

                # TODO: process RowCode.START_LOCATION_EXT (startup location metadata)

            elif row_code == AptDat.RowCode.WINDSOCK:
                logger.debug("Parsing sign row.")

                windsock = Windsock.from_line(row)

                if windsock is not None:
                    self.windsocks.append(windsock)

            elif row_code == AptDat.RowCode.TAXI_SIGN:
                logger.debug("Parsing sign row.")

                sign = Sign.from_line(row)

                if sign is not None:
                    self.signs.append(sign)

            elif row_code == AptDat.RowCode.TAXIWAY:
                logger.debug("Parsing pavement row.")

                pavement = Pavement.from_row_iterator(
                    row, row_iterator, bezier_resolution
                )

                if pavement is not None:
                    self.pavements.append(pavement)

            elif row_code == AptDat.RowCode.FREE_CHAIN:
                logger.debug("Parsing linear feature row.")

                for line in LinearFeature.from_row_iterator(
                    row, row_iterator, bezier_resolution
                ):
                    if line is not None:
                        self.linear_features.append(line)

    def export(
        self,
        output_path: Union[str, Path],
        driver: Optional[str] = None,
        crs: str = "EPSG:4326",
        features: list[str] = VALID_FEATURES,
    ) -> None:
        """Export the parsed airport in a GIS-friendly format.

        Args:
            output_path (str, Path): File path for the output.
                Note that with some drivers (like GeoJSON) multiple files will be generated (one per feature).
            driver (str): OGR driver (file format) to use for the output.
                See `xplane_apt_convert.base.SUPPORTED_DRIVERS.keys()` for a list of valid options.
                If `None`, then the driver will be automatically inferred from the file extension in `output_path`.
                Default `None`.
            crs (str): Coordinate reference system (CRS) to use for the output.
                Default "EPSG:4326".
            features (list[str]): List of feature layers to include in the output.
                See `xplane_apt_convert.base.VALID_FEATURES` for a list of valid options.
                Default is all.
        """
        if driver is not None and driver not in SUPPORTED_DRIVERS:
            raise ValueError(
                f"Invalid driver '{driver}'. Supported drivers: {list(SUPPORTED_DRIVERS.keys())}"
            )

        if (
            isinstance(output_path, str)
            and len(output_path) > 0
            and output_path[-1] == "/"
        ):
            raise ValueError("output_path cannot be a directory.")

        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        suffix = output_path.suffix

        if not suffix and not driver:
            raise ValueError(
                "Unknown output driver. Output path must have a valid file extension or an explicit driver must be provided."
            )

        if driver is None:
            driver = _detect_driver(output_path)

            if driver is None:
                raise ValueError(
                    f"Format {output_path.suffix} not recognized. Provide a valid file extension or specify an explicit driver."
                )

        base_folder = output_path.parent
        base_name = output_path.stem

        if not suffix:
            suffix = "." + SUPPORTED_DRIVERS[driver]["default_extension"]

        base_folder.mkdir(parents=True, exist_ok=True)

        for part_name in features:
            if part_name not in VALID_FEATURES:
                raise ValueError(
                    f"{part_name} is not a valid include. Valid options are: {VALID_FEATURES}"
                )

            part = getattr(self, part_name)

            if not part:
                logger.warning(f"No {part_name} found.")
                continue

            logger.info(f"Writing {part_name}.")

            part_type = get_type_hints(ParsedAirport)[part_name]
            part_type_origin = get_origin(part_type)
            part_type_args = get_args(part_type)

            part_is_list = get_origin(part_type) == list

            if part_type_origin == list:
                part_is_list = True
                schema = part_type_args[0]._schema()
            elif part_type_origin == Union:
                assert len(part_type_args) == 2 and part_type_args[1] == type(
                    None
                )  # Only Unions equivalent to Optional are valid.

                part_is_list = False
                schema = part_type_args[0]._schema()
            else:
                part_is_list = False
                schema = part_type._schema()

            multilayer = SUPPORTED_DRIVERS[driver]["multilayer"]

            if multilayer:
                path = base_folder / f"{base_name}{suffix}"
                layer = part_name
            else:
                path = base_folder / f"{base_name}.{part_name}{suffix}"
                layer = None

            with fiona.open(
                path,
                mode="w",
                crs=crs,
                driver=driver,
                schema=schema,
                layer=layer,
            ) as output:
                if part_is_list:
                    records = [record._to_record() for record in part]
                else:
                    records = [part._to_record()]

                if _BASE_CRS != crs:
                    for record in records:
                        record["geometry"] = transform_geom(
                            _BASE_CRS, crs, record["geometry"]
                        )

                output.writerecords(records)
