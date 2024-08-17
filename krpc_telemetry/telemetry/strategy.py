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


class OrbitalVelocityStrategy(TelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("orbital_velocity", "Orbital Velocity", collect_every_secs)

    def get_telemetry_types(self) -> Set[TelemetryType]:
        return {TelemetryType.MET, TelemetryType.ORBITAL_SPEED}

    def _collect_data(self, met: int, data: Dict[TelemetryType, Any]):
        collected_data_dataframe = pd.DataFrame({
            TelemetryType.MET: met,
            TelemetryType.ORBITAL_SPEED: data[TelemetryType.ORBITAL_SPEED]
        }, index=[0])
        collected_data_dataframe.set_index(TelemetryType.MET, inplace=True)
        self._dataframe = pd.concat(
            [
                self._dataframe,
                collected_data_dataframe
            ]) if len(self._dataframe) else collected_data_dataframe

    def get_telemetry_plot(self):
        plot: Figure =  self._dataframe.plot()
        scatter_0: Scatter = cast(Scatter, plot.data[0])
        scatter_0.line.shape = "spline"
        return plot


class SurfaceVelocityStrategy(TelemetryStrategy, ABC):
    def __init__(self, collect_every_secs: int = 1):
        super().__init__("surface_velocity", "Surface Velocity", collect_every_secs)

    def get_telemetry_types(self) -> Set[TelemetryType]:
        return {TelemetryType.MET, TelemetryType.SURFACE_SPEED}

    def _collect_data(self, met: int, data: Dict[TelemetryType, Any]):
        collected_data_dataframe = pd.DataFrame({
            TelemetryType.MET: met,
            TelemetryType.SURFACE_SPEED: data[TelemetryType.SURFACE_SPEED]
        }, index=[0])
        collected_data_dataframe.set_index(TelemetryType.MET, inplace=True)
        self._dataframe = pd.concat(
            [
                self._dataframe,
                collected_data_dataframe
            ]) if len(self._dataframe) else collected_data_dataframe

    def get_telemetry_plot(self) -> Figure:
        plot: Figure =  self._dataframe.plot()
        scatter_0: Scatter = cast(Scatter, plot.data[0])
        scatter_0.line.shape = "spline"
        return plot
