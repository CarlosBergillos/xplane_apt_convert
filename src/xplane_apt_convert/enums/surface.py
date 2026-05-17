from ._fallback import FallbackEnum


class SurfaceType(FallbackEnum):
    ASPHALT = 1  # Asphalt
    CONCRETE = 2  # Concrete
    TURF_OR_GRASS = 3  # Turf or grass
    DIRT = 4  # Dirt (brown)
    GRAVEL = 5  # Gravel (grey)
    DRY_LAKEBED = 12  # Dry lakebed
    WATER_RUNWAY = 13  # Water runway
    SNOW_OR_ICE = 14  # Snow or ice
    TRANSPARENT = 15  # Transparent


class ShoulderSurfaceType(FallbackEnum):
    NONE = 0  # No shoulder
    ASPHALT = 1  # Asphalt shoulder
    CONCRETE = 2  # Concrete shoulder
