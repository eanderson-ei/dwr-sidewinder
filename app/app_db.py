import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_table
import pandas as pd

from app import app, db


### ----------------------------- LAYOUT --------------------------------- ###

_option_list = db.inspect(db.engine).get_table_names()
options = [
    {'label': option, 'value': option} for option in _option_list
]

layout = html.Div([
    dbc.Container(
        [
            dcc.Dropdown(
                id='select_table',
                options=options,
                placeholder="Select Table",
                multi=False
                ),
            html.Br(), html.Br(),
            html.Div(id='postgres_datatable')
        ],
    )
]
)


### ---------------------------- CALLBACKS ------------------------------- ###

@app.callback(Output('postgres_datatable', 'children'),
              [Input('select_table', 'value')])
def populate_datatable(table_select):
    if not table_select:
        raise PreventUpdate
    else:
        df = pd.read_sql_table(table_select, con=db.engine)
        return [
            dash_table.DataTable(
                id='our-table',
                columns=[{
                            'name': str(x),
                            'id': str(x),
                            'deletable': False,
                        } 
                        for x in df.columns],
                data=df.to_dict('records'),
                editable=True,
                row_deletable=True,
                filter_action="native",
                sort_action="native",  # give user capability to sort columns
                sort_mode="single",  # sort across 'multi' or 'single' columns
                page_action='none',  # render all of the data at once. No paging.
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'center'
                    } for c in ['id']
                ]

            ),
        ]
    