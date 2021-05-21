import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_daq as daq
import plotly.express as px
import folium
import pandas as pd

from app import app, db


### ----------------------------- SETUP ---------------------------------- ###

# Test Data
df = pd.read_sql_table('view_cosmos_targets', conn=db.engine)

def plot_cosmos(df):
    fig = px.bar(df, x='habitat_type', y='quantity', color='cpa_name',
                 title='Conservation Strategy Measurable Objective Contributions')
    fig.update_layout(barmode='relative')
    return fig

### ----------------------------- LAYOUT --------------------------------- ###

### SELECT REGION ###
_regions = [
    'Upper Sacramento River',
    'Lower Sacramento River',
    'Feather River',
    'Lower Sacramento/Delta North',
    'Upper San Joaquin River'
]
_region_options = [{'label': region, 'value': region} for region in _regions]

select_region = dcc.Dropdown(
    id='select-region',
    placeholder='Select a CPA or RFMP',
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
location = [36.872839, -119.857740]

def create_map(location):        
    m = folium.Map(location=location,
                    tiles='Stamen Terrain',
                    width='100%',
                    height='100%',
                    prefer_canvas=True,
                    zoom_control=False)
    
    return m.get_root().render()

map = html.Iframe(
    id='map', 
    srcDoc=create_map(location), 
    height='400',
    style={'background': '#FFFFFF', 'border': '0'}
    )


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
layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col([
                select_region, 
                cosmos_chart, 
                dbc.Row(date_slider, justify='center', align='center')
                ], width=8
            ),
            dbc.Col([
                dbc.Row(map, justify='center', align='center'),
                html.Br(),
                projects_card
                ], width=4
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
        fig = plot_cosmos(df[filt])
    else:
        fig = plot_cosmos(df)
    return fig