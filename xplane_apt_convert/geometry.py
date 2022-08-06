import numpy as np
from bezier.curve import Curve
from xplane_airports.AptDat import RowCode

_DEFAULT_BEZIER_RESOLUTION = 16


def _calculate_quadratic_bezier(p0, p1, p2, resolution):
    if p0 == p2:
        return [p0]

    curve = Curve.from_nodes(np.asarray([p0, p1, p2]).T)
    curve_points = curve.evaluate_multi(np.linspace(0.0, 1.0, resolution))

    return curve_points.T.tolist()


def _calculate_cubic_bezier(p0, p1, p2, p3, resolution):
    if p0 == p3:
        return [p0]

    curve = Curve.from_nodes(np.asarray([p0, p1, p2, p3]).T)
    curve_points = curve.evaluate_multi(np.linspace(0.0, 1.0, resolution))

    return curve_points.T.tolist()


def _calculate_bezier(p0, p1, p2, p3=None, resolution=_DEFAULT_BEZIER_RESOLUTION):
    if p3 is None:
        return _calculate_quadratic_bezier(p0, p1, p2, resolution)
    else:
        return _calculate_cubic_bezier(p0, p1, p2, p3, resolution)


def get_paths(row_iterator, bezier_resolution, mode="line"):
    # https://forums.x-plane.org/index.php?/forums/topic/66713-understanding-the-logic-of-bezier-control-points-in-aptdat/

    assert mode == "line" or mode == "polygon"

    coordinates = []
    properties = {}

    def _start_segment():
        nonlocal coordinates, properties
        coordinates = []
        properties = {}

    def _finish_segment():
        nonlocal coordinates, properties
        if len(coordinates) > 1:
            # simplify line. remove consecutive duplicates
            prev_c = None
            fixed_coordinates = []
            for c in coordinates:
                if prev_c is not None and tuple(c) == tuple(prev_c):
                    continue

                fixed_coordinates.append(c)

                prev_c = c

            coordinates_list.append(fixed_coordinates)
            properties_list.append(properties)

    def _process_row(is_bezier, tokens):
        nonlocal in_bezier, temp_bezier_nodes, coordinates, properties
        lat, lon = float(tokens[1]), float(tokens[2])

        if not is_bezier:
            if in_bezier:
                temp_bezier_nodes.append((lon, lat))
                coordinates.extend(
                    _calculate_bezier(*temp_bezier_nodes)
                )  # TODO: pass resolution argument
                temp_bezier_nodes = []
            else:
                coordinates.append((lon, lat))

            in_bezier = False

            painted_line_type = int(tokens[3]) if len(tokens) > 3 else None
            lighting_line_type = int(tokens[4]) if len(tokens) > 4 else None

            if mode == "line" and (
                (
                    painted_line_type is not None
                    and properties.get("painted_line_type") is not None
                    and painted_line_type != properties["painted_line_type"]
                )
                or (
                    lighting_line_type is not None
                    and properties.get("lighting_line_type") is not None
                    and lighting_line_type != properties["lighting_line_type"]
                )
            ):
                if row_iterator.has_next():
                    _finish_segment()
                    _start_segment()
                    row_iterator.unnext()  # reuse row for the new segment
            else:
                if painted_line_type is not None:
                    properties["painted_line_type"] = painted_line_type

                if lighting_line_type is not None:
                    properties["lighting_line_type"] = lighting_line_type

        else:
            bzp_lat, bzp_lon = float(tokens[3]), float(tokens[4])

            if in_bezier:
                diff_lat = bzp_lat - lat
                diff_lon = bzp_lon - lon
                mirr_lat = lat - diff_lat
                mirr_lon = lon - diff_lon

                temp_bezier_nodes.append((mirr_lon, mirr_lat))
                temp_bezier_nodes.append((lon, lat))
                coordinates.extend(
                    _calculate_bezier(*temp_bezier_nodes, resolution=bezier_resolution)
                )
                temp_bezier_nodes = []
            else:
                if len(coordinates):
                    diff_lat = bzp_lat - lat
                    diff_lon = bzp_lon - lon
                    mirr_lat = lat - diff_lat
                    mirr_lon = lon - diff_lon

                    temp_bezier_nodes.append(coordinates[-1])
                    temp_bezier_nodes.append((mirr_lon, mirr_lat))
                    temp_bezier_nodes.append((lon, lat))
                    coordinates.extend(
                        _calculate_bezier(
                            *temp_bezier_nodes, resolution=bezier_resolution
                        )
                    )
                    temp_bezier_nodes = []

            temp_bezier_nodes.append((lon, lat))
            temp_bezier_nodes.append((bzp_lon, bzp_lat))

            # else:
            in_bezier = True

            painted_line_type = int(tokens[5]) if len(tokens) > 5 else None
            lighting_line_type = int(tokens[6]) if len(tokens) > 6 else None

            if mode == "line" and (
                (
                    painted_line_type is not None
                    and properties.get("painted_line_type") is not None
                    and painted_line_type != properties["painted_line_type"]
                )
                or (
                    lighting_line_type is not None
                    and properties.get("lighting_line_type") is not None
                    and lighting_line_type != properties["lighting_line_type"]
                )
            ):
                if row_iterator.has_next():
                    _finish_segment()
                    _start_segment()
                    row_iterator.unnext()  # reuse row for the new segment
            else:
                if painted_line_type is not None:
                    properties["painted_line_type"] = painted_line_type

                if lighting_line_type is not None:
                    properties["lighting_line_type"] = lighting_line_type

    coordinates_list = []
    properties_list = []
    more_segments = True

    while more_segments:
        temp_bezier_nodes = []
        in_bezier = False
        first_row = None
        first_row_is_bezier = None

        _start_segment()

        for row in row_iterator:
            if first_row is None:
                first_row = row
                first_row_is_bezier = row.row_code in [
                    RowCode.LINE_CURVE,
                    RowCode.RING_CURVE,
                    RowCode.END_CURVE,
                ]

            row_code = row.row_code
            tokens = row.tokens

            if row_code == RowCode.LINE_SEGMENT:
                _process_row(False, tokens)
            elif row_code == RowCode.LINE_CURVE:
                _process_row(True, tokens)
            elif row_code == RowCode.RING_SEGMENT:
                _process_row(False, tokens)
                _process_row(first_row_is_bezier, first_row.tokens)
                break
            elif row_code == RowCode.RING_CURVE:
                _process_row(True, tokens)
                _process_row(first_row_is_bezier, first_row.tokens)
                break
            elif row_code == RowCode.END_SEGMENT:
                _process_row(False, tokens)
                break
            elif row_code == RowCode.END_CURVE:
                _process_row(True, tokens)
                break
            else:
                row_iterator.unnext()
                more_segments = False
                break
        else:
            # there is no more rows
            more_segments = False

        _finish_segment()

    assert len(coordinates_list) == len(properties_list)
    return coordinates_list, properties_list
