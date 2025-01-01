import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
import pandas as pd

# Fetch data from the backend
response = requests.get("http://localhost:5000/api/network_activity")
data = response.json()
df = pd.DataFrame(data)

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    html.H1("Network Activity Dashboard"),
    dcc.Graph(id='network-activity-graph'),
    dcc.Dropdown(
        id='filter',
        options=[
            {'label': 'Applications', 'value': 'app'},
            {'label': 'Traffic Types', 'value': 'traffic_type'}
        ],
        value='app',
        clearable=False
    ),
    html.Div(id='details', style={'marginTop': 20}),
    html.H2("Connected Devices"),
    html.Button("Refresh Devices", id="refresh-devices"),
    html.Ul(id="devices-list")
])

# Callbacks
@app.callback(
    Output('network-activity-graph', 'figure'),
    Input('filter', 'value')
)
def update_graph(filter_value):
    fig = px.line(df, x='time', y='bytes', color=filter_value, markers=True)
    return fig

@app.callback(
    Output('details', 'children'),
    Input('network-activity-graph', 'clickData')
)
def display_click_data(clickData):
    if clickData:
        point = clickData['points'][0]
        selected_data = df[(df['time'] == point['x']) & (df['bytes'] == point['y'])].iloc[0]
        return html.Div([
            html.H4(f"Details for {selected_data['app']}"),
            html.P(f"Host: {selected_data['host']}"),
            html.P(f"Country: {selected_data['country']}"),
            html.P(f"Bytes: {selected_data['bytes']}")
        ])
    return "Click on a point in the graph to see details."

@app.callback(
    Output('devices-list', 'children'),
    Input('refresh-devices', 'n_clicks')
)
def update_devices_list(n_clicks):
    if n_clicks:
        response = requests.get("http://localhost:5000/api/devices")
        print(response.status_code, response.text)  # Debugging output
        devices = response.json()
        if not devices:
            return [html.Li("No devices found")]
        return [html.Li(f"{device['host']} ({device['hostname']}) - {device['state']}") for device in devices]
    return [html.Li("Click 'Refresh Devices' to scan for connected devices")]

if __name__ == '__main__':
    app.run_server(debug=True)
