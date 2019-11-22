from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app= Flask(__name__)
app.config['SECRET_KEY'] = 'youwontguess'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOG_TO_STDOUT'] = os.environ.get('LOG_TO_STDOUT')

db = SQLAlchemy(app)
Migrate(app,db)

app.static_folder = 'static'

from project.routes import admin

app.register_blueprint(admin)