__version__ = '0.0.16'

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from home.config import TEMPLATE_FOLDER, STATIC_FOLDER
from home.dash.api import api
from home.dash.web import web
from home.ts.models import db, Graph, Series, Device, DeviceSeries, Area


def create_app(config=None):

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER)

    app.config['SECRET_KEY'] = 'ssh, its a secret.'

    app.config.from_object('home.config')
    app.config.from_object(config)

    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')

    db.init_app(app)

    Migrate(app, db, directory='home/migrations')

    admin = Admin(app)
    admin.add_view(ModelView(Area, db.session))
    admin.add_view(ModelView(Device, db.session))
    admin.add_view(ModelView(Series, db.session))
    admin.add_view(ModelView(DeviceSeries, db.session))
    admin.add_view(ModelView(Graph, db.session))

    return app

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)
