from ._fallback import FallbackEnum


class SurfaceType(FallbackEnum):
    ASPHALT = 1  # Asphalt nr. 1
    CONCRETE = 2  # Concrete nr. 1
    TURF_OR_GRASS = 3  # Turf or grass
    DIRT = 4  # Dirt (brown)
    GRAVEL = 5  # Gravel (grey)
    DRY_LAKEBED = 12  # Dry lakebed
    WATER_RUNWAY = 13  # Water runway (deprecated, use sealane rowcode)
    SNOW_OR_ICE = 14  # Snow or ice
    TRANSPARENT = 15  # Transparent
    LIGHT_COLORED_ASPHALT_1 = 20  # Light colored asphalt nr. 1
    LIGHT_COLORED_ASPHALT_2 = 21  # Light colored asphalt nr. 2
    LIGHT_COLORED_ASPHALT_3 = 22  # Light colored asphalt nr. 3
    LIGHT_COLORED_ASPHALT_4 = 23  # Light colored asphalt nr. 4
    ASPHALT_2 = 24  # Asphalt nr. 2
    ASPHALT_3 = 25  # Asphalt nr. 3
    ASPHALT_4 = 26  # Asphalt nr. 4
    DARK_COLORED_ASPHALT_1 = 27  # Darker colored asphalt nr. 1
    DARK_COLORED_ASPHALT_2 = 28  # Darker colored asphalt nr. 2
    DARK_COLORED_ASPHALT_3 = 29  # Darker colored asphalt nr. 3
    DARK_COLORED_ASPHALT_4 = 30  # Darker colored asphalt nr. 4
    VERY_DARK_COLORED_ASPHALT_1 = 31  # Very dark colored asphalt nr. 1
    VERY_DARK_COLORED_ASPHALT_2 = 32  # Very dark colored asphalt nr. 2
    VERY_DARK_COLORED_ASPHALT_3 = 33  # Very dark colored asphalt nr. 3
    VERY_DARK_COLORED_ASPHALT_4 = 34  # Very dark colored asphalt nr. 4
    NEAR_BLACK_ASPHALT_1 = 35  # Near black, 'new' looking asphalt nr. 1
    NEAR_BLACK_ASPHALT_2 = 36  # Near black, 'new' looking asphalt nr. 2
    NEAR_BLACK_ASPHALT_3 = 37  # Near black, 'new' looking asphalt nr. 3
    NEAR_BLACK_ASPHALT_4 = 38  # Near black, 'new' looking asphalt nr. 4
    LIGHT_CONCRETE_1 = 50  # Light 'new' looking concrete nr. 1
    LIGHT_CONCRETE_2 = 51  # Light 'new' looking concrete nr. 2
    LIGHT_CONCRETE_3 = 52  # Light 'new' looking concrete nr. 3
    CONCRETE_2 = 53  # Concrete nr. 2
    CONCRETE_3 = 54  # Concrete nr. 3
    DARK_CONCRETE_1 = 55  # Dark concrete nr. 1
    DARK_CONCRETE_2 = 56  # Dark concrete nr. 2
    DARK_CONCRETE_3 = 57  # Dark concrete nr. 3


class ShoulderSurfaceType(FallbackEnum):
    NONE = 0  # No shoulder
    ASPHALT = 1  # Asphalt shoulder
    CONCRETE = 2  # Concrete shoulder
