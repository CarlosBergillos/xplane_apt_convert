# X-Plane apt.dat convert

<a href="https://pypi.org/project/xplane-apt-convert/" target="_blank">
    <img src="https://img.shields.io/pypi/v/xplane_apt_convert.svg" alt="Package version">
</a>
<a href="https://pypi.org/project/xplane-apt-convert/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/xplane_apt_convert.svg" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/xplane-apt-convert/" target="_blank">
    <img src="https://img.shields.io/pypi/wheel/xplane_apt_convert.svg" alt="Wheel support">
</a>
<a href="https://pypi.org/project/xplane-apt-convert/" target="_blank">
    <img src="https://img.shields.io/pypi/l/xplane_apt_convert.svg" alt="License">
</a>

`xplane_apt_convert` is a Python package and CLI application allowing to convert X-Plane airport data to GIS-friendly formats like GeoJSON or ESRI Shapefile.

[![Example LELL airport layout](https://raw.githubusercontent.com/CarlosBergillos/xplane_apt_convert/main/images/example_LEBL.png)](https://raw.githubusercontent.com/CarlosBergillos/xplane_apt_convert/main/images/example_LEBL.png)


## Input

X-Plane `apt.dat` files are used as input.
Two input modes exist:

- Load a local `apt.dat` file.
- Automatically download airport-specific files from the [X-Plane Scenery Gateway](https://gateway.x-plane.com/).

**Note:** Only tested with `apt.dat` files version 1100.


## Output

The following output formats are supported:

| Format                     | Extension   |
| :------------------------- | :---------- |
| ESRI Shapefile             | `.shp`      |
| FlatGeobuf                 | `.fgb`      |
| GeoJSON                    | `.geojson`  |
| GeoJSON lines (GeoJSONSeq) | `.geojsonl` |
| GeoPackage (GPKG)          | `.gpkg`     |
| GML                        | `.gml`      |
| OGR_GMT                    | `.gmt`      |
| SQLite                     | `.sqlite`   |


## Supported Features

The following airport features are supported:

- **Windsocks** (row code `19`)
- **Ground signs** (row code `20`)
- **Runways** (row code `100`)
- **Pavement areas (taxiway and aprons)** (header row code `110`)
- **Ground markings (linear features)** (header row code `120`)
- **Airport boundary** (header row code `130`)
- **Aircraft startup locations (parking and gates)** (row code `1300`)
- **Airport metadata** (row code `1302`)


## Installation

The `xplane_apt_convert` Python package can be installed using pip:

```console
pip install xplane_apt_convert
```

**Python 3.10 and above**

When using Python 3.10 and above, you might encounter the following error during the installation of the `bezier` dependency:
`The BEZIER_INSTALL_PREFIX environment variable must be set.`

To solve it, you can install the pure Python version of the `bezier` package by running:

```console
BEZIER_NO_EXTENSION=true pip install bezier --no-binary=bezier
```

And then try installing `xplane_apt_convert` again.

See [dhermes/bezier/issues/283](https://github.com/dhermes/bezier/issues/283) for more details about this issue.


## CLI Basic Usage

Convert an airport in a local `apt.dat` file to GeoJSON:

```console
python -m xplane_apt_convert -a LEBL -i ./apt.dat -o ./out/ -d GeoJSON
```


Convert multiple airports:

```console
python -m xplane_apt_convert -a LEBL,LEGE,LERS,LELL -i ./apt.dat -o ./out/ -d GeoJSON
```


Download the recommended airport data files from the X-Plane Scenery Gateway and convert them:

```console
python -m xplane_apt_convert -a LEBL,LEGE,LERS,LELL -g -o ./out/ -d GeoJSON
```

Other output file formats are available using the `-d` option, for example `GeoJSON`, `ESRI Shapefile`, or `GPKG`.

For information about all available options run the command using `--help`.

[![CLI help](https://raw.githubusercontent.com/CarlosBergillos/xplane_apt_convert/main/images/cli_help.svg)](https://raw.githubusercontent.com/CarlosBergillos/xplane_apt_convert/main/images/cli_help.svg)


## Python Basic Usage

Convert an airport in a local `apt.dat` file to GeoJSON:

```python
from xplane_airports.AptDat import AptDat
from xplane_apt_convert import ParsedAirport

input_file = "./apt.dat"
airport_id = "LEBL"

with open(input_file, "r") as f:
    apt_dat = AptDat.from_file_text(f.read(), input_file)

apt = apt_dat.search_by_id(airport_id)

p_apt = ParsedAirport(apt)
p_apt.export("./airport.geojson")
```


Download an airport from the X-Plane Scenery Gateway and convert it to ESRI Shapefile:

```python
from xplane_airports.gateway import scenery_pack
from xplane_apt_convert import ParsedAirport

airport_id = "LEBL"

recommended_pack = scenery_pack(airport_id)
apt = recommended_pack.apt

p_apt = ParsedAirport(apt)
p_apt.export("./airport.shp", driver="ESRI Shapefile")
```

See the function's docstring for more information on all the allowed arguments.


## License

This software is licensed under the terms of the [MIT License](LICENSE).
