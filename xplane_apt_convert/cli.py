from pathlib import Path
from typing import Optional

import rich.progress
import typer
from click.exceptions import UsageError
from requests import HTTPError
from xplane_airports.AptDat import AptDat
from xplane_airports.gateway import scenery_pack

from .base import SUPPORTED_DRIVERS, VALID_FEATURES, ParsedAirport
from .geometry import _DEFAULT_BEZIER_RESOLUTION

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_short=True,
)


@app.command()
def convert(
    airport_ids: str = typer.Option(
        ...,
        "--airport-ids",
        "-a",
        help="Comma separated list of airport IDs of the airports to parse and convert "
        + "(note that these are X-Plane airport IDs, usually matching the ICAO codes, but not always).",
    ),
    input_file: Optional[Path] = typer.Option(
        None,
        "--input-file",
        "-i",
        help="Input airport data (apt.dat) file path.",
        file_okay=True,
        dir_okay=False,
        readable=True,
        exists=True,
    ),
    download_recommended: bool = typer.Option(
        False,
        "--download-recommended",
        "-g",
        help="Download recommended airport files from the X-Plane Scenery Gateway "
        + "instead of using a local file.",
    ),
    output_folder: Path = typer.Option(
        "./",
        "--output-folder",
        "-o",
        help="Output folder.",
        file_okay=False,
        dir_okay=True,
        writable=True,
        exists=False,
    ),
    driver: str = typer.Option(
        "GeoJSON",
        "--driver",
        "-d",
        help=f"Format driver to use for the output. Supported drivers: {', '.join(SUPPORTED_DRIVERS.keys())}.",
        case_sensitive=False,
    ),
    crs: str = typer.Option(
        "EPSG:4326",
        "--crs",
        "-c",
        help="Coordinate reference system (CRS) to use for the output.",
    ),
    features: str = typer.Option(
        ",".join(VALID_FEATURES),
        "--features",
        "-f",
        help="Comma separated list of feature layers to include in the output.",
    ),
    bezier_resolution: int = typer.Option(
        _DEFAULT_BEZIER_RESOLUTION,
        "--bezier-resolution",
        "-z",
        help="Number of points to use to plot Bezier curves. "
        + "A higher number means more resolution but also larger file sizes.",
    ),
):
    """
    Convert X-Plane airport data to GIS-friendly formats like GeoJSON or ESRI Shapefile.

    Airports will either be loaded from a local apt.dat file (when using '--input-file' / '-i')
    or downloaded from the X-Plane Scenery Gateway (when using '--download-recommended' / '-g').
    """
    if airport_ids is None or airport_ids == "":
        raise UsageError("List of airport ids cannot be empty.")

    if input_file is not None and download_recommended:
        raise UsageError(
            "Only one of --input_file and --download_recommended can be used."
        )

    if input_file is None and not download_recommended:
        raise UsageError("Either --input_file or --download_recommended must be used.")

    apt_dat = None

    if input_file is not None:
        with rich.progress.open(input_file, "r") as f:
            apt_dat = AptDat.from_file_text(f.read(), input_file)

    for airport_id in rich.progress.track(
        airport_ids.split(","), description="Processing airports..."
    ):
        if apt_dat is not None:
            apt = apt_dat.search_by_id(airport_id)

            if apt is None:
                # logger.error(f"Airport {airport_id} not found in {input_file}.")
                print(f"Airport '{airport_id}' not found in {input_file}.")
                raise typer.Abort()

        else:
            assert download_recommended
            try:
                recommended_pack = scenery_pack(airport_id, retries_on_error=0)
            except HTTPError as e:
                print(e.__dict__)
                print(f"Failed to download '{airport_id}' ({e}).")
                continue

            apt = recommended_pack.apt

        extension = SUPPORTED_DRIVERS[driver]["default_extension"]
        output_file = output_folder / f"{airport_id}.{extension}"

        p_apt = ParsedAirport(apt, bezier_resolution=bezier_resolution)
        p_apt.export(output_file, driver=driver, crs=crs, features=features.split(","))
