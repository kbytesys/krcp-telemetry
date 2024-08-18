from enum import StrEnum, auto


class TelemetryType(StrEnum):
    MET = auto()
    ORBITAL_SPEED = auto()
    SURFACE_SPEED = auto()
