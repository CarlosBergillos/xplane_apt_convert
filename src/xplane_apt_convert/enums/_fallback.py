import logging
from enum import Enum, EnumMeta


logger = logging.getLogger("xplane_apt_convert")

logged_unknowns = set()


class FallbackEnumMeta(EnumMeta):
    class Fallback:
        def __init__(self, name):
            self.name = name

    def __call__(cls, value, *args, **kwargs):
        try:
            return EnumMeta.__call__(cls, value, *args, **kwargs)
        except ValueError:
            if value is None:
                return FallbackEnumMeta.Fallback(None)
            else:
                if (cls, value) not in logged_unknowns:
                    logger.warning(f"Unknown value {value} found for {cls.__name__}.")
                    # do not log same warning many times
                    logged_unknowns.add((cls, value))

                return FallbackEnumMeta.Fallback(f"UNKNOWN_{value}")


class FallbackEnum(Enum, metaclass=FallbackEnumMeta):
    """Custom subclass of Enum that supports handling of arbitrary unknown values."""
