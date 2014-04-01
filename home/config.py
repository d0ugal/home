from logging.config import dictConfig
from os import path
from sys import stdout

SQLALCHEMY_DATABASE_URI = 'postgresql://home:home@localhost:5432/home'

PROJECT_PATH = path.dirname(path.realpath(__file__))
TEMPLATE_FOLDER = path.join(PROJECT_PATH, 'dash', 'templates')
STATIC_FOLDER = path.join(PROJECT_PATH, 'dash', 'static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s %(name)-35s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'rfxcom': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'home': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        }
    },
}

dictConfig(LOGGING)


PACKET_HANDLERS = {
    'rfxcom.protocol.Status': 'home.collect.logging_handler',
    'rfxcom.protocol.Elec': 'home.collect.elec_handler',
    'rfxcom.protocol.TempHumidity': 'home.collect.temp_humidity_handler',
    '*': 'home.collect.logging_handler',
}
