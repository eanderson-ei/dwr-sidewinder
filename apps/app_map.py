import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_leaflet as dl
from dash_extensions.javascript import arrow_function
import pandas as pd
import plotly.express as px
from dash_extensions.javascript import Namespace
import dash_leaflet.express as dlx

from app import app, db


### ----------------------------- SETUP ---------------------------------- ###
df = pd.read_sql_table('view_project_outcomes', con=db.engine)

# get project locations
def get_data(cpa: int):
    df_cpa = df[df['cpa_name'] == cpa] if cpa else df
    df_cpa = df_cpa[['project_nickname', 'cpa_name', 'coordinate_x', 'coordinate_y']].dropna()
    dicts = df_cpa.to_dict('rows')
    for item in dicts:
        item['tooltip'] = item['project_nickname']
        item['popup'] = item['cpa_name']
    geojson = dlx.dicts_to_geojson(dicts, lat='coordinate_x', lon="coordinate_y")
    geobuf = dlx.geojson_to_geobuf(geojson)
    return geobuf

# create cpa dropdown    
cpas = df['cpa_name'].unique()
cpa_options = [{'label': cpa, 'value': cpa} for cpa in cpas]
dd_cpa = dcc.Dropdown(options=cpa_options, id='dd_cpa')

# set up scatter points
ns = Namespace('dlx', 'scatter')
geojson = dl.GeoJSON(data=get_data(None), id='geojson', format='geobuf',
                     zoomToBounds=True,
                     cluster=True,
                    #  clusterToLayer=ns("clusterToLayer"),
                     zoomToBoundsOnClick=True,
                    #  options=dict(pointToLayer=ns('pointToLayer')),
                     superClusterOptions=dict(radius=150))
                    #  hideout=dict(colorscale='Viridis', colorProp='cpa'))

# add cpa boundaries
cpa_boundaries = dl.GeoJSON(id='rfmp',
                            url="/assets/rfmp4.json", 
                            zoomToBounds=True,                            
                            hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')))  # must be in assets folder 

# create map
map = dl.Map([dl.TileLayer(), cpa_boundaries, geojson])

# create dropdown for CPA
dd = html.Div([dd_cpa], style={"position": "relative", "bottom": "80px", "left": "10px", "z-index": "1000", "width": "200px"})

table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


layout = html.Div(
    [
        map, dd, dbc.Row(dbc.Col(id='state')), dbc.Row(dbc.Col(table, width={'size': 10, 'offset': 1}))
    ], 
    style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "position": "relative"})

### ----------------------------- LAYOUT --------------------------------- ###

# ### MAP ###
# location = [36.872839, -119.857740]

# map = dl.Map(center=location, zoom=6, children=[
#     dl.TileLayer(),
#     dl.GeoJSON(url="/assets/rfmp4.json", zoomToBounds=True, id='rfmp',
#                hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),  # must be in assets folder
#     ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, 
#     id="map")

# ### LAYOUT ###
# layout = html.Div(
#     [
#         dbc.Row(dbc.Col(map), justify='center'),
#         dbc.Row(dbc.Col(id="state", width={'size': 11, 'offset': 1}))
#     ]
# )

# ### ---------------------------- CALLBACKS ------------------------------- ###

@app.callback(Output("state", "children"), [Input("rfmp", "hover_feature")])
def state_hover(feature):
    if feature is not None:
        return f"{feature['properties']['Region']}"
    
@app.callback(Output('geojson', 'data'),
              [Input('dd_cpa', 'value')])
def update_map(cpa):
    return get_data(cpa)