"""
home.config
===========

The default settings.
"""
from logging.config import dictConfig
from os import path
from sys import stdout

#: The database connection string.
SQLALCHEMY_DATABASE_URI = 'postgresql://home:home@localhost:5432/home'

PROJECT_PATH = path.dirname(path.realpath(__file__))

#: Location of the dashboard templates.
TEMPLATE_FOLDER = path.join(PROJECT_PATH, 'dash', 'templates')
#: Location of the dashboard static assets.
STATIC_FOLDER = path.join(PROJECT_PATH, 'dash', 'static')

#: Location of the Alembic database migrations.
MIGRATE_DIRECTORY = path.join(PROJECT_PATH, 'migrations')

#: The default location for the warning log.
LOG_WARNING_FILENAME = path.join(PROJECT_PATH, "home-warning.log")

#: The default location for the full log.
LOG_FULL_FILENAME = path.join(PROJECT_PATH, "home.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)-8s %(name)-35s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'standard'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': LOG_WARNING_FILENAME,
            'maxBytes': 10 * 1024 * 1024,
        },
        'file-full': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': LOG_FULL_FILENAME,
            'maxBytes': 10 * 1024 * 1024,
        },
    },
    'loggers': {
        'rfxcom': {
            'handlers': ['console', 'file', 'file-full'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'home': {
            'handlers': ['console', 'file', 'file-full'],
            'propagate': True,
            'level': 'DEBUG',
        }
    },
}

dictConfig(LOGGING)

DEBUG_TB_INTERCEPT_REDIRECTS = False

#: The default packet handlers, the devices that will be recorded by default.
PACKET_HANDLERS = {
    'rfxcom.protocol.Status': 'home.collect.logging_handler',
    'rfxcom.protocol.Elec': 'home.collect.elec_handler',
    'rfxcom.protocol.TempHumidity': 'home.collect.temp_humidity_handler',
    '*': 'home.collect.logging_handler',
}
