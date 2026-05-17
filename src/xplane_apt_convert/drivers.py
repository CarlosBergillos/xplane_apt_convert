from pathlib import Path


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


VALID_FEATURES = [
    "boundary",
    "runways",
    "startup_locations",
    "windsocks",
    "signs",
    "pavements",
    "linear_features",
]


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
