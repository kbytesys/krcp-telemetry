import argparse
import json

import pandas as pd
import krpc

from krpc_telemetry.dashboard import init_dashboard
from krpc_telemetry.krpc_streams import KrpcTelemetryStreamFactory, init_streams_from_telemetry_processor
from krpc_telemetry.processor_builder import TelemetryProcessorBuilder

pd.options.plotting.backend = "plotly"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='krpc_telemetry', description="Simple Kerbal Telemetry using KRPC")
    parser.add_argument("config", type=open, help="KRPC telemetry configuration file")
    parser.add_argument("--address", type=str, help="KRPC server address", default="localhost")
    parser.add_argument("--rpc-port", type=int, help="KRPC server port", default=50000)
    parser.add_argument("--streaming-port", type=int, help="KRPC server port", default=50001)
    args = parser.parse_args()

    config = json.load(args.config)

    conn = krpc.connect(name='KRPC-Telemetry', address=args.address,
                        rpc_port=args.rpc_port, stream_port=args.streaming_port)

    try:
        vessel = conn.space_center.active_vessel
    except ValueError:
        print("No active vessel for telemetry recording, exiting")
        exit(1)

    krpc_telemetry_factory = KrpcTelemetryStreamFactory(vessel, conn)
    telemetry_processor = TelemetryProcessorBuilder.build_processor(config)
    telemetry_collection = init_streams_from_telemetry_processor(telemetry_processor, krpc_telemetry_factory)
    telemetry_processor.start_processor_thread(telemetry_collection)
    try:
        init_dashboard(telemetry_processor).run(debug=True, use_reloader=False)
    finally:
        telemetry_processor.stop_processor_thread()
        print("exiting")
