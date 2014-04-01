from argparse import ArgumentParser

from home import app
from home.collect.handlers import RecordingHander, LoggingHandler
from home.collect.loop import collect


elec_handler = RecordingHander({
    'electricity': 'current_watts',
    'total_watts': 'total_watts'
})

temp_humidity_handler = RecordingHander({
    'temperature': 'temperature',
    'humidity': 'humidity'
})

logging_handler = LoggingHandler()


parser = ArgumentParser(description='.')
parser.add_argument('--device')


def run():

    args = parser.parse_args()

    with app.app_context():
        collect(args.device)
