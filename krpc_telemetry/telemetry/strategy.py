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


class SingleValueTelemetryStrategy(TelemetryStrategy, ABC):
    def __init__(self, name: str, title: str, telemetry_type: TelemetryType, collect_every_secs: int = 1):
        super().__init__(name, title, collect_every_secs)
        self._telemetry_type = telemetry_type

    def get_telemetry_types(self) -> Set[TelemetryType]:
        return {TelemetryType.MET, self._telemetry_type}

    def _collect_data(self, met: int, data: Dict[TelemetryType, Any]):
        collected_data_dataframe = pd.DataFrame({
            TelemetryType.MET: met,
            self._telemetry_type: data[self._telemetry_type]
        }, index=[0])
        collected_data_dataframe.set_index(TelemetryType.MET, inplace=True)
        self._dataframe = pd.concat(
            [
                self._dataframe,
                collected_data_dataframe
            ]) if len(self._dataframe) else collected_data_dataframe

    def get_telemetry_plot(self):
        plot: Figure = self._dataframe.plot()
        scatter_0: Scatter = cast(Scatter, plot.data[0])
        scatter_0.line.shape = "spline"
        return plot


class OrbitalVelocityStrategy(SingleValueTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("orbital_velocity", "Orbital Velocity", TelemetryType.ORBITAL_SPEED, collect_every_secs)


class SurfaceVelocityStrategy(SingleValueTelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("surface_velocity", "Surface Velocity", TelemetryType.SURFACE_SPEED, collect_every_secs)
