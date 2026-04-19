from ._fallback import FallbackEnum


class SignSize(FallbackEnum):
    SMALL = 1  # Small taxiway sign
    MEDIUM = 2  # Medium taxiway sign
    LARGE = 3  # Large taxiway sign
    LARGE_DISTANCE_REMAINING = 4  # Large distance-remaining sign on runway edge
    SMALL_DISTANCE_REMAINING = 5  # Small distance-remaining sign on runway edg
