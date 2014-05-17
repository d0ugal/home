"""
home.config
===========

The default settings.
"""
from os import path

PROJECT_PATH = path.dirname(path.realpath(__file__))

#: The database connection string.
SQLALCHEMY_DATABASE_URI = 'postgresql://home:home@localhost:5432/home'

#: Location of the dashboard templates.
TEMPLATE_FOLDER = path.join(PROJECT_PATH, 'dash', 'templates')

#: Location of the dashboard static assets.
STATIC_FOLDER = path.join(PROJECT_PATH, 'dash', 'static')

#: Location of the uploaded/dynamic files.
MEDIA_FOLDER = path.join(STATIC_FOLDER, 'media')

#: Location of the Alembic database migrations.
MIGRATE_DIRECTORY = path.join(PROJECT_PATH, 'migrations')

#: The default location for the warning log.
LOG_WARNING_FILENAME = path.join(PROJECT_PATH, "home-warning.log")

#: The default location for the full log.
LOG_FULL_FILENAME = path.join(PROJECT_PATH, "home.log")

#: The default packet handlers, the devices that will be recorded by default.
PACKET_HANDLERS = {
    'rfxcom.protocol.Elec': 'home.collect.elec_handler',
    'rfxcom.protocol.TempHumidity': 'home.collect.temp_humidity_handler',
    '*': 'home.collect.logging_handler',
}

DEBUG_TB_INTERCEPT_REDIRECTS = False

CONFIG_SAMPLE = path.join(PROJECT_PATH, 'conf', 'config.py.sample')
SUPERVISOR_SAMPLE = path.join(PROJECT_PATH, 'conf', 'supervisord.conf')
NGINX_SAMPLE = path.join(PROJECT_PATH, 'conf', 'nginx.conf')
