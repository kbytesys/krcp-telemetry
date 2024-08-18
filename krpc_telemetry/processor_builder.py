from typing import Any

from krpc_telemetry.telemetry.processor import TelemetryProcessor
from krpc_telemetry.telemetry.strategy import OrbitalVelocityStrategy, SurfaceVelocityStrategy


class TelemetryProcessorBuilder:
    @staticmethod
    def build_processor(config: Any) -> TelemetryProcessor:
        result = TelemetryProcessor()

        for telemetry in config.get("telemetry"):
            if telemetry.get("name") == "orbital_velocity":
                result.add_strategy(OrbitalVelocityStrategy())
            elif telemetry.get("name") == "surface_velocity":
                result.add_strategy(SurfaceVelocityStrategy())
            else:
                raise ValueError(f"Unknown telemetry name: {telemetry.name}")

        return result

