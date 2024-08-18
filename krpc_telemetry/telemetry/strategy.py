from abc import ABC, abstractmethod
from typing import Dict, Any, Set, cast

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from plotly.graph_objs import Figure, Scatter

from krpc_telemetry.telemetry import TelemetryType


class TelemetryStrategy(ABC):
    def __init__(self, name: str, title: str, collect_every_secs: int = 1):
        self._collect_every_secs = collect_every_secs
        self._lastMet = -1
        self._dataframe = pd.DataFrame()
        self.name = name
        self.title = title
        self.plot: Figure | None = None

    def collect_data(self, met: int, data: Dict[TelemetryType, Any]) -> None:
        if self._lastMet != -1 and self._collect_every_secs + self._lastMet > met:
            return

        self._lastMet = met
        self._collect_data(met, data)

    @property
    def dataframe(self) -> DataFrame:
        return self._dataframe

    @abstractmethod
    def _collect_data(self, met: int, data: Dict[TelemetryType, Any]) -> None:
        pass

    @abstractmethod
    def get_telemetry_types(self) -> Set[TelemetryType]:
        pass

    @abstractmethod
    def get_telemetry_plot(self) -> Figure:
        pass


class GenericTelemetryStrategy(TelemetryStrategy, ABC):
    def __init__(self, name: str, title: str, telemetry_types: list[TelemetryType], collect_every_secs: int = 1):
        super().__init__(name, title, collect_every_secs)
        self._telemetry_types = telemetry_types

    def get_telemetry_types(self) -> Set[TelemetryType]:
        return {TelemetryType.MET, *self._telemetry_types}

    def _collect_data(self, met: int, data: Dict[TelemetryType, Any]):
        collected_data = dict()

        collected_data[TelemetryType.MET] = met

        for telemetry_type in self._telemetry_types:
            collected_data[telemetry_type] = data[telemetry_type]

        collected_data_dataframe = pd.DataFrame(collected_data, index=[0])
        collected_data_dataframe.set_index(TelemetryType.MET, inplace=True)
        self._dataframe = pd.concat(
            [
                self._dataframe,
                collected_data_dataframe
            ]) if len(self._dataframe) else collected_data_dataframe

    def get_telemetry_plot(self):
        plot: Figure = self._dataframe.plot()
        for index in range(0, len(plot.data)):
            set_spline_line(plot.data[index])
        return plot


class OrbitalVelocityStrategy(GenericTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("orbital_velocity", "Orbital Velocity", [TelemetryType.ORBITAL_SPEED], collect_every_secs)


class SurfaceVelocityStrategy(GenericTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("surface_velocity", "Surface Velocity",
                         [TelemetryType.SURFACE_SPEED,
                          TelemetryType.SURFACE_HORIZONTAL_SPEED,
                          TelemetryType.SURFACE_VERTICAL_SPEED]
                         , collect_every_secs)


class OrbitApoEpiStrategy(GenericTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("orbit_apo_peri", "Orbital Apoapsis and Periapsis",
                         [TelemetryType.ORBITAL_APOAPSIS, TelemetryType.ORBITAL_PERIAPSIS], collect_every_secs)


class AtmospherePressureStrategy(GenericTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("atm_pressure", "Atmosphere pressure and forces",
                         [TelemetryType.ATMOSPHERE_DENSITY,
                          TelemetryType.DYNAMIC_PRESSURE,
                          TelemetryType.STATIC_PRESSURE]
                         , collect_every_secs)


class GForceStrategy(GenericTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("gforce", "G-Force", [TelemetryType.G_FORCE], collect_every_secs)


def set_spline_line(data: Any) -> None:
    scatter_0: Scatter = cast(Scatter, data)
    scatter_0.line.shape = "spline"
