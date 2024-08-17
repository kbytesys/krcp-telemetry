import threading
from time import sleep
from typing import List, Set, Dict, Any

from pandas.core.interchange.dataframe_protocol import DataFrame

from krpc_telemetry.telemetry import TelemetryType
from krpc_telemetry.telemetry.strategy import TelemetryStrategy


class TelemetryProcessor:
    def __init__(self):
        self._processor_loop_thread = None
        self._telemetry_collection = None
        self._strategies: List[TelemetryStrategy] = []
        self._run_thread = False

    @property
    def strategies(self):
        return self._strategies

    def add_strategy(self, strategy: TelemetryStrategy):
        self._strategies.append(strategy)

    def get_telemetry_types(self) -> Set[TelemetryType]:
        result = set()
        for strategy in self._strategies:
            for telemetry_type in strategy.get_telemetry_types():
                if telemetry_type not in result:
                    result.add(telemetry_type)

        return result

    def process_telemetry_data(self, data: Dict[TelemetryType, Any]):
        met = data[TelemetryType.MET]
        for strategy in self._strategies:
            strategy.collect_data(met, data)

    def get_telemetry_data(self) -> Dict[str, DataFrame]:
        result = dict()
        for strategy in self._strategies:
            result[strategy.name] = strategy.dataframe

        return result

    def get_telemetry_data_single(self, name: str) -> DataFrame | None:
        for strategy in self._strategies:
            if strategy.name == name:
                return strategy.dataframe

        return None

    def _processor_loop_thread_function(self):
        while self._run_thread:
            sleep(1)
            collected_data = self._telemetry_collection.collect_data()
            self.process_telemetry_data(collected_data)

    def start_processor_thread(self, telemetry_collection):
        if self._run_thread:
            return
        self._run_thread = True

        self._telemetry_collection = telemetry_collection
        self._telemetry_collection.start_telemetries()

        self._processor_loop_thread = threading.Thread(target=self._processor_loop_thread_function)
        self._processor_loop_thread.start()

    def stop_processor_thread(self):
        if not self._run_thread:
            return
        self._run_thread = False

        self._telemetry_collection.destroy_telemetries()
        self._processor_loop_thread.join()
