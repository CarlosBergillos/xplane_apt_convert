from ._fallback import FallbackEnum


class RunwayMarking(FallbackEnum):
    NONE = 0  # No runway markings
    VISUAL = 1  # Visual markings
    NON_PRECISION = 2  # Non-precision approach markings
    PRECISION = 3  # Precision approach markings
    UK_NON_PRECISION = 4  # UK-style non-precision approach markings
    UK_PRECISION = 5  # UK-style precision approach markings


class ApproachLighting(FallbackEnum):
    NONE = 0  # No approach lighting
    ALSF_I = 1  # ALSF-I. Approach Lighting System with Sequenced Flashing Lights
    ALSF_II = 2  # ALSF-II. Approach Lighting System with Sequenced Flashing Lights
    CALVERT = 3  # Calvert
    CALVERT_II = 4  # Calvert ILS Cat II and Cat II
    SSALR = 5  # SSALR. Simplified Short Approach Lighting System with Runway Alignment Indicator Lights
    SSALF = 6  # SSALF. Simplified Short Approach Lighting System with Sequenced Flashing Lights
    SALS = 7  # SALS. Short Approach Light System
    MALSR = 8  # MALSR. Medium-intensity Approach Light System with Runway Alignment Indicator Lights
    MALSF = 9  # MALSF. Medium-intensity Approach Light System with Sequenced Flashing Lights
    MALS = 10  # MALS. Medium-intensity Approach Light System
    ODALS = 11  # ODALS. Omni-Directional Approach Light System
    RAIL = 12  # RAIL. Runway Alignment Indicator Lights


class RunwayEndIdentifierLights(FallbackEnum):
    NONE = 0  # No REIL
    OMNIDIRECTIONAL_REIL = 1  # Omni-directional REIL
    UNIDIRECTIONAL_REIL = 2  # Unidirectional REIL
