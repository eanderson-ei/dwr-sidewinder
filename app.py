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

ENV = 'local'

if ENV == 'deploy':
    app.server.debug = False
    uri = os.environ['DATABASE_URL']
    uri = uri.replace("postgres://", "postgresql://", 1)
    app.server.config['SQLALCHEMY_DATABASE_URI'] = uri  # Heroku needs to update URI for newer versions of Postgres

elif ENV == 'local':
    app.server.debug = True
    with open('secrets/db_uri.txt') as f:
        uri = f.read()
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.server.config['SQLALCHEMY_DATABASE_URI'] = uri
elif ENV == 'test':
    app.server.debug = True
    app.server.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://postgres:incentives@localhost/dwr_test'
# avoids warning in console
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app.server)

# from app import routes

