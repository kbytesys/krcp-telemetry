from dash import Dash, html, dcc, Output, Input

from krpc_telemetry.telemetry.processor import TelemetryProcessor


def init_dashboard(telemetry_processor: TelemetryProcessor) -> Dash:
    app = Dash()

    def serve_layout():
        return html.Div([
            html.H1('KRPC Telemetry', className="inline-component"),
            html.Button(id='start-stop-button', children='Pause', className="inline-component"),
            html.Div([
                html.H4('Orbital Speed'),
                dcc.Graph(id='orbital-speed-graph'),
            ]),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ]
        )


    app.layout = serve_layout


    @app.callback(Output('orbital-speed-graph', 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        dataframe = telemetry_processor.get_telemetry_data_single("orbital_velocity")
        if dataframe is None:
            return None

        return dataframe.plot()


    @app.callback(Output('interval-component', 'disabled'),
                  Output('start-stop-button', 'children'),
                  Input('start-stop-button', 'n_clicks'),
                  Input('interval-component', 'disabled'))
    def callback_func_start_stop_interval(n_clicks, disabled_state):
        if not n_clicks:
            return False, "Pause"
        return (True, "Resume") if not disabled_state and n_clicks > 0 else (False, "Pause")

    return app
