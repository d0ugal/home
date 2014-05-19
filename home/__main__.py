"""
home.__main__
=============

This module is the entry point for the application and is responsible for
defining the custom sub commands for the ``home`` command line interface.

"""
from datetime import datetime, timedelta
from logging.config import dictConfig
from sys import stdout
from warnings import warn

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server, prompt_pass

from home import create_app, db
from home.collect.loop import collect as rfxcom_collect
from home.dash.models import User
from home.webcam.loop import collect as webcam_collect

app = create_app()

manager = Manager(app, with_default_commands=False)

manager.add_command('db', MigrateCommand)
manager.add_command("dashboard", Server(host='0.0.0.0', use_debugger=False,
                    use_reloader=False))


@manager.option('--device', help='Serial device.')
def rfxcom(device):
    """Start the event loop to collect data from the serial device."""

    # If the device isn't passed in, look for it in the config.
    if device is None:
        device = app.config.get('DEVICE')

    # If the device is *still* none, error.
    if device is None:
        print("The serial device needs to be passed in as --device or "
              "set in the config as DEVICE.")
        return

    rfxcom_collect(device)


@manager.option('--device', help='Serial device.')
def collect(device):
    warn("The collect command is deprecated. Use the rfxcom command instead.",
         DeprecationWarning)
    rfxcom(device)


@manager.command
def webcam():
    webcam_collect()


@manager.option('username', help='Username.')
def create_user(username):
    "Create a new user."
    password = prompt_pass("Enter password")
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()


@manager.command
def config_sample():
    print(open(app.config['CONFIG_SAMPLE']).read())


@manager.command
def supervisor_sample():
    print(open(app.config['SUPERVISOR_SAMPLE']).read())


@manager.command
def nginx_sample():
    print(open(app.config['NGINX_SAMPLE']).read())


@manager.command
def populate_redis():

    from home.ts.models import DataPoint
    from home import redis_series

    redis_series._redis.flushall()

    now = datetime.utcnow()

    limit = now - timedelta(days=7)

    start = limit
    end = limit + timedelta(hours=1)

    while end < now:

        print(start, limit)

        data_points = DataPoint.query.filter(
            DataPoint.created_at >= start,
            DataPoint.created_at <= end,
        ).order_by(DataPoint.created_at.desc())

        for data_point in data_points:
            data_point.push_to_redis()

        start = start + timedelta(hours=1)
        end = end + timedelta(hours=1)


def main():

    DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)-8s %(name)-35s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'stream': stdout,
                'formatter': 'standard'
            },
            'file': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': app.config['LOG_WARNING_FILENAME'],
                'maxBytes': 10 * 1024 * 1024,
            },
            'file-full': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': app.config['LOG_FULL_FILENAME'],
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

    LOGGING = app.config.get('LOGGING', DEFAULT_LOGGING)

    dictConfig(LOGGING)

    manager.run()

if __name__ == '__main__':
    main()
