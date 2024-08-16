# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation
# import pandas as pd
#
# pd.options.plotting.backend = "plotly"
#
# fig, axs = plt.subplots(1, 2, layout='constrained')
#
# data_frame = pd.DataFrame(columns=["a", "b", "c"])
#
# row_to_append = pd.DataFrame([{"a": 1, "b": 2, "c": 3}])
# data_frame = pd.concat([data_frame, row_to_append], ignore_index=True)
# row_to_append = pd.DataFrame([{"a": 6, "b": 4, "c": 7}, {"a": 9, "b": 9, "c": 9}])
# data_frame = pd.concat([data_frame, row_to_append], ignore_index=True)
#
# for col in data_frame.columns:
#     print(data_frame.get(col).tolist())
#
# print(data_frame)
# print("miao")
# #print(data_frame.drop(index=data_frame.index[[0]], inplace=True))
# data_frame = data_frame.truncate(before=1)
# print("miao")
# print(data_frame)
#
# row_to_append = pd.DataFrame([{"a": 1, "b": 2, "c": 3}])
# data_frame = pd.concat([data_frame, row_to_append], ignore_index=True)
# print(data_frame)
#
# fig = data_frame.plot()
# fig.show()

from time import sleep

from krpc_telemetry.telemetry import TelemetryType
from krpc_telemetry.krpc_streams import KrpcTelemetryStreamFactory, KrpcTelemetryStreamCollection, \
    init_streams_from_telemetry_processor

import krpc

from krpc_telemetry.telemetry.processor import TelemetryProcessor
from krpc_telemetry.telemetry.strategy import OrbitalVelocityStrategy

conn = krpc.connect(name='KRPC-Telemetry', address='172.24.240.1', rpc_port=50000, stream_port=50001)

try:
    vessel = conn.space_center.active_vessel
except ValueError:
    print("No active vessel for telemetry recording, exiting")
    exit(1)

krpc_telemetry_factory = KrpcTelemetryStreamFactory(vessel, conn)
telemetry_processor = TelemetryProcessor()
telemetry_processor.add_strategy(OrbitalVelocityStrategy())
telemetry_collection = init_streams_from_telemetry_processor(telemetry_processor, krpc_telemetry_factory)

while True:
    sleep(1)
    collected_data = telemetry_collection.collect_data()
    print("Data collected at %s %s" % (TelemetryType.MET, collected_data[TelemetryType.MET]))
    telemetry_processor.process_telemetry_data(collected_data)



