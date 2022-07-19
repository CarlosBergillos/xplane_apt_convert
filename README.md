# X-Plane apt.dat convert

Convert X-Plane airport data to GIS-friendly formats like GeoJSON or ESRI Shapefile.

![CLI help](./images/example_LEBL.png)

## Supported Output Formats

| Format                     | Extension |
| :------------------------- | :-------- |
| ESRI Shapefile             | .shp      |
| FlatGeobuf                 | .fgb      |
| GeoJSON                    | .geojson  |
| GeoJSON lines (GeoJSONSeq) | .geojsonl |
| GeoPackage (GPKG)          | .gpkg     |
| GML                        | .gml      |
| OGR_GMT                    | .gmt      |
| SQLite                     | .sqlite   |


## Supported Features

- Airport boundary
- Runways
- Pavement areas (taxiway and aprons)
- Ground markings (linear features)
- Ground signs
- Aircraft startup locations (parking and gates)
- Windsocks


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

![CLI help](./images/cli_help.svg)


## Python Basic Usage

Convert an airport in a local `apt.dat` file to GeoJSON:

```python
from xplane_airports.AptDat import AptDat

with open(input_file, "r") as f:
    apt_dat = AptDat.from_file_text(f.read(), input_file)

p_apt = ParsedAirport(apt)
p_apt.export("./aiport.geojson"")
```


Download an airport from the X-Plane Scenery Gateway and convert it to ESRI Shapefile:

```python
from xplane_airports.gateway import scenery_pack
from xplane_airport_convert import ParsedAirport

recommended_pack = scenery_pack(airport_id)
apt = recommended_pack.apt

p_apt = ParsedAirport(apt)
p_apt.export("./aiport.shp", driver="GeoJSON")
```
