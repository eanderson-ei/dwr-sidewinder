from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc
import os


external_stylesheets = [dbc.themes.YETI]

server = Flask(__name__)
app = dash.Dash(__name__, server=server, 
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)

ENV = 'deploy'

if ENV == 'dev':
    app.server.debug = True
    app.server.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://postgres:incentives@localhost/test2'
else:
    app.server.debug = False
    app.server.config['SQLALCHEMY_DATBASE_URI'] = os.environ['DATABASE_URL']

# avoids warning in console
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app.server)

# from app import routes

