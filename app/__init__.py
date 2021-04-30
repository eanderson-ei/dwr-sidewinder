from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:incentives@localhost/test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATBASE_URI'] = ''

# avoids warning in console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# from app import routes