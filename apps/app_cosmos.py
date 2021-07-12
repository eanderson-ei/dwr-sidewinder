import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_daq as daq
import dash_leaflet as dl
from dash_extensions.javascript import Namespace
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import app, db


### ----------------------------- SETUP ---------------------------------- ###

# Load data
cosmos_targets = pd.read_sql_table('view_cosmos_targets', con=db.engine)
project_outcomes = pd.read_sql_table('view_project_outcomes', con=db.engine)

# prep data for chart
df = project_outcomes.merge(
    cosmos_targets[['cpa_name', 'long_form', 'quantity']], 
    how='right',
    on=['cpa_name', 'long_form'])

df['contribution'] = df['total_outcomes'] / df['quantity']


def plot_cosmos(df):
    
    
    
    fig = go.Figure()
    bar_width = .7
    
    fig.add_traces(go.Bar(
            x=df['contribution'],
            y=df['long_form'],
            name='Outcomes',
            orientation='h',
            width=bar_width
        ))

    fig.update_layout(barmode='stack')
    
    
    return fig


def get_project_points(cpa: str):
    df_cpa = project_outcomes[project_outcomes['cpa_name'] == cpa] if cpa else project_outcomes
    df_cpa = df_cpa[['project_nickname', 'cpa_name', 'coordinate_x', 'coordinate_y']].dropna().drop_duplicates()
    dicts = df_cpa.to_dict('rows')
    for item in dicts:
        item['tooltip'] = item['project_nickname']
        item['popup'] = item['cpa_name']
    geojson = dlx.dicts_to_geojson(dicts, lat='coordinate_x', lon="coordinate_y")
    return dlx.geojson_to_geobuf(geojson)




### ----------------------------- LAYOUT --------------------------------- ###

### SELECT REGION ###
_regions = cosmos_targets['cpa_name'].unique()
_region_options = [{'label': region, 'value': region} for region in _regions]

select_region = dcc.Dropdown(
    id='select-region',
    placeholder='Select a CPA',
    options=_region_options
)

### COSMOS CHART ###
cosmos_chart = dcc.Graph(
    id='cosmos-chart',
    config = {
        'displayModeBar': 'hover',
        'doubleClick': False,
        'scrollZoom': False,
        'modeBarButtonsToRemove': [
            'zoom2d', 'select2d', 'lasso2d', 
            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 
            'resetScale2d', 'hoverClosestCartesian',
            'hoverCompareCartesian'
            ],
        'displaylogo': False
    }
)

### DATE RANGE SLIDER ###
date_slider = daq.Slider(
    id='date-slider',
    min=5,
    max=15,
    handleLabel={"showCurrentValue": True, "label": "yr"},
    updatemode='mouseup',
    color='blue',
    size = 265*2,
    marks={'5': '5 yr', '10': '10 yr', '15': 'Beyond'}
)


### MAP ###

# set up scatter points
ns = Namespace('dlx', 'scatter')
geojson = dl.GeoJSON(data=get_project_points(None), id='geojson', format='geobuf',
                     zoomToBounds=True,
                     cluster=True,
                     zoomToBoundsOnClick=True,
                     superClusterOptions=dict(radius=150))

# add cpa boundaries
cpa_boundaries = dl.GeoJSON(id='rfmp',
                            url="/assets/cpa.json", 
                            zoomToBounds=True,                            
                            hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')))  # must be in assets folder 

# create map
map = dl.Map(id='map', 
             children= [dl.TileLayer(), cpa_boundaries, geojson],
             style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})


### PROJECT WINDOW ###
_projects = [
    'Project A',
    'Project B',
    'Project C',
    'Project D'
]

projects_card = dbc.Card(
    dbc.CardBody(
        dcc.Checklist(
            options = [{'label': "\t" + project, 'value': project} for project in _projects],
            labelStyle={'display': 'block'}
        )
    )
)


### LAYOUT ###
layout = html.Div(
    dbc.Row(
        [
            dbc.Col([
                select_region, 
                cosmos_chart, 
                dbc.Row(date_slider, justify='center', align='center')
                ], width={'size': 7, 'offset': 1}
            ),
            dbc.Col([
                map
                ], width=3
            )
        ]
    )
)

### ---------------------------- CALLBACKS ------------------------------- ###

@app.callback(
    Output('cosmos-chart', 'figure'),
    [Input('select-region', 'value')]
)
def update_chart(region):
    if region:
        filt = df['cpa_name'] == region
        return plot_cosmos(df[filt])
    else:
        return plot_cosmos(df)