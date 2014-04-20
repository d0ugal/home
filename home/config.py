from logging.config import dictConfig
from os import path
from sys import stdout

SQLALCHEMY_DATABASE_URI = 'postgresql://home:home@localhost:5432/home'

PROJECT_PATH = path.dirname(path.realpath(__file__))
TEMPLATE_FOLDER = path.join(PROJECT_PATH, 'dash', 'templates')
STATIC_FOLDER = path.join(PROJECT_PATH, 'dash', 'static')

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
            'filename': path.join(PROJECT_PATH, "home.log"),
            'maxBytes': 10 * 1024 * 1024,
        },
        'file-full': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': path.join(PROJECT_PATH, "home-full.log"),
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

DEBUG_TB_INTERCEPT_REDIRECTS = False

dictConfig(LOGGING)


PACKET_HANDLERS = {
    'rfxcom.protocol.Status': 'home.collect.logging_handler',
    'rfxcom.protocol.Elec': 'home.collect.elec_handler',
    'rfxcom.protocol.TempHumidity': 'home.collect.temp_humidity_handler',
    '*': 'home.collect.logging_handler',
}
