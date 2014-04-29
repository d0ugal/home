__version__ = '0.1.1'

from os import environ

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import LoginManager, current_user
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()


class AuthedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()


def create_app(config=None):
    """ This needs some tidying up. To avoid circular imports we import
    everything here but it makes this method a bit more gross.
    """

    # Initialise the app
    from home.config import TEMPLATE_FOLDER, STATIC_FOLDER
    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER)

    app.config['SECRET_KEY'] = 'ssh, its a secret.'

    # Load the default config, the specified config file and then any
    # overwrites that are manually passed in.
    app.config.from_object('home.config')

    if 'HOME_SETTINGS' in environ:
        app.config.from_envvar('HOME_SETTINGS')

    app.config.from_object(config)

    # Register the web front end and the API.
    from home.dash.web import web
    from home.dash.api import api
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')

    login_manager.init_app(app)
    login_manager.login_view = 'Dashboard Web.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialise the migrations app, we want to store all migrations within
    # the project directory for easier packaging.
    Migrate(app, db, directory='home/migrations')

    # Wire up the models to flask admin
    from home.ts.models import Graph, Series, Device, DeviceSeries, Area
    from home.dash.models import User

    admin = Admin(app)
    admin.add_view(AuthedModelView(Area, db.session))
    admin.add_view(AuthedModelView(Device, db.session))
    admin.add_view(AuthedModelView(Series, db.session))
    admin.add_view(AuthedModelView(DeviceSeries, db.session))
    admin.add_view(AuthedModelView(Graph, db.session))

    admin.add_view(AuthedModelView(User, db.session))

    # Wire up the database to the app so it gets the config.
    db.init_app(app)

    return app
