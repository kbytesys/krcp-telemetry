from typing import List, Set, Dict, Any

from krpc_telemetry.telemetry import TelemetryType
from krpc_telemetry.telemetry.strategy import TelemetryStrategy


class TelemetryProcessor:
    def __init__(self):
        self._strategies: List[TelemetryStrategy] = []

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

