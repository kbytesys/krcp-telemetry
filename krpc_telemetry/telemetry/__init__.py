from enum import StrEnum, auto


class TelemetryType(StrEnum):
    MET = auto()
    ORBITAL_APOAPSIS = auto()
    ORBITAL_PERIAPSIS = auto()
    ORBITAL_SPEED = auto()
    SURFACE_SPEED = auto()
