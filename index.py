from app import app, db

from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import os

from apps import app_db, app_cosmos


### ---------------------------- NAV BAR ------------------------------- ###

# Nav Bar
LOGO = app.get_asset_url('logo.png')  # update logo.png in assets/

# nav item links
nav_items = dbc.Container([
    dbc.NavItem(dbc.NavLink('Cosmos', href='/')),
    dbc.NavItem(dbc.NavLink('Database', href='/db'))
]
)

# navbar with logo
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo/brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("DWR Sidewinder", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",  # comment out to remove main page link
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_items], className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5"
)

### ---------------------------- LAYOUT ------------------------------- ###

# Layout placeholder
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


### ---------------------------- CALLBACKS ------------------------------- ###

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return app_cosmos.layout
    elif pathname == '/db':
         return app_db.layout
    # elif pathname == '/apps/app2':
    #      return layout2
    else:
        return '404'
    
    
if __name__== '__main__':
    app.run_server(debug=True)
