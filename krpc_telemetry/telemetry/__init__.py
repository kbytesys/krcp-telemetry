from enum import StrEnum, auto


class TelemetryType(StrEnum):
    ATMOSPHERE_DENSITY = auto()
    AERODYNAMIC_FORCE = auto()
    CENTER_OF_MASS = auto()
    DYNAMIC_PRESSURE = auto()
    G_FORCE = auto()
    MET = auto()
    ORBITAL_APOAPSIS = auto()
    ORBITAL_PERIAPSIS = auto()
    ORBITAL_SPEED = auto()
    STATIC_PRESSURE = auto()
    SURFACE_SPEED = auto()
    SURFACE_HORIZONTAL_SPEED = auto()
    SURFACE_VERTICAL_SPEED = auto()
