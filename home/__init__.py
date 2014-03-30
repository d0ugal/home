__version__ = '0.0.4'

from flask import Flask

from home.dash.web import web
from home.dash.api import api
from home.ts.models import db
from home.config import TEMPLATE_FOLDER, STATIC_FOLDER

app = Flask(__name__,
            static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

app.config.from_object('home.config')
app.register_blueprint(web)
app.register_blueprint(api, url_prefix='/api')

db.init_app(app)
