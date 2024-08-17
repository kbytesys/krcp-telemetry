from typing import List

from dash import Dash, html, dcc, Output, Input

from krpc_telemetry.telemetry.processor import TelemetryProcessor


def add_update_graph_callback(app: Dash, telemetry_processor: TelemetryProcessor, graph_name: str):
    @app.callback(Output('%s-graph' % graph_name, 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        return telemetry_processor.get_telemetry_plot(graph_name)


def add_graph_html_block(graph_name: str, graph_title) -> html.Div:
    return html.Div([
        html.H2(graph_title, className="text-lg"),
        dcc.Graph(id='%s-graph' % graph_name),
    ], className="basis-1/2 p-2")


def create_graphs_and_interval_callbacks(app: Dash, telemetry_processor: TelemetryProcessor) -> List[html.Div]:
    result = []
    for strategy in telemetry_processor.strategies:
        result.append(add_graph_html_block(strategy.name, strategy.title))
        add_update_graph_callback(app, telemetry_processor, strategy.name)
    return result


def init_dashboard(telemetry_processor: TelemetryProcessor) -> Dash:
    app = Dash(
        external_scripts=["https://cdn.tailwindcss.com"]
    )

    graph_layout = create_graphs_and_interval_callbacks(app, telemetry_processor)

    def serve_layout():
        return html.Div([
            html.H1('KRPC Telemetry', className="inline-block text-2xl"),
            html.Button(id='start-stop-button', children='Pause', className="inline-block font-bold ml-4 py-2 px-4 rounded bg-blue-500 text-white"),
            html.Button(id='shutdown-button', children='Shutdown', className="inline-block font-bold ml-4 py-2 px-4 rounded bg-blue-500 text-white"),
            html.Div(
                graph_layout, className="mt-4 flex flex-wrap"
            ),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ], className="p-4"
        )

    app.layout = serve_layout

    @app.callback(Output('interval-component', 'disabled', allow_duplicate=True),
                  Output('start-stop-button', 'children'),
                  Input('start-stop-button', 'n_clicks'),
                  Input('interval-component', 'disabled'), prevent_initial_call=True)
    def callback_func_start_stop_interval(n_clicks, disabled_state):
        if not n_clicks:
            return False, "Pause"
        return (True, "Resume") if not disabled_state and n_clicks > 0 else (False, "Pause")

    @app.callback(Output('interval-component', 'disabled', allow_duplicate=True),
                  Input('shutdown-button', 'n_clicks'), prevent_initial_call=True)
    def callback_func_shutdown(n_clicks):
        if not n_clicks:
            return False, "Pause"
        telemetry_processor.stop_processor_thread()
        return True

    return app
