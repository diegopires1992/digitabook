from flask import Flask
from os import getenv

from config import config_selector
from app.configurations import database, migration, authentication, commands, serialization
from app import views
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(f'config.{config_selector[config]}')
    commands.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    authentication.init_app(app)
    views.init_app(app)
    serialization.init_app(app)


    return app
