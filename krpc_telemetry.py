import pandas as pd
import krpc

from krpc_telemetry.dashboard import init_dashboard
from krpc_telemetry.krpc_streams import KrpcTelemetryStreamFactory, init_streams_from_telemetry_processor
from krpc_telemetry.telemetry.processor import TelemetryProcessor
from krpc_telemetry.telemetry.strategy import OrbitalVelocityStrategy, SurfaceVelocityStrategy

pd.options.plotting.backend = "plotly"


if __name__ == '__main__':
    conn = krpc.connect(name='KRPC-Telemetry', address='172.24.240.1')

    try:
        vessel = conn.space_center.active_vessel
    except ValueError:
        print("No active vessel for telemetry recording, exiting")
        exit(1)

    krpc_telemetry_factory = KrpcTelemetryStreamFactory(vessel, conn)
    telemetry_processor = TelemetryProcessor()
    telemetry_processor.add_strategy(OrbitalVelocityStrategy())
    telemetry_processor.add_strategy(SurfaceVelocityStrategy())
    telemetry_collection = init_streams_from_telemetry_processor(telemetry_processor, krpc_telemetry_factory)
    telemetry_processor.start_processor_thread(telemetry_collection)
    try:
        init_dashboard(telemetry_processor).run(debug=True, use_reloader=False)
    finally:
        telemetry_processor.stop_processor_thread()
        print("exiting")
