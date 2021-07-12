import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash
from dash.dependencies import Output, Input
from dash_extensions.javascript import arrow_function

# Generate some in-memory data.
bermuda = dlx.dicts_to_geojson([dict(lat=32.299507, lon=-64.790337)])
biosfera = dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=29.015, lon=-118.271)]))
# Create example app.
app = Dash()
app.layout = html.Div([
    dl.Map(center=[39, -98], zoom=4, children=[
        dl.TileLayer(),
        dl.GeoJSON(url="/assets/rfmp4.json"),  # geojson resource (faster than in-memory)
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
    html.Div(id="state"), html.Div(id="capital")
])

if __name__ == '__main__':
    app.run_server(debug=True)