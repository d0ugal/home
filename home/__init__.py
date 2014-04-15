__version__ = '0.0.11'

from flask import Flask

from home.config import TEMPLATE_FOLDER, STATIC_FOLDER
from home.dash.api import api
from home.dash.web import web
from home.ts.models import db


def create_app(config=None):
    app = Flask(__name__,
                static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

    app.config['SECRET_KEY'] = 'ssh, its a secret.'

    app.config.from_object('home.config')
    app.config.from_object(config)

    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')

    db.init_app(app)

    return app

app = create_app()
