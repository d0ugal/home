from argparse import ArgumentParser

from rfxcom import protocol

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


def run():

    parser = ArgumentParser(description='.')
    parser.add_argument('--device')

    args = parser.parse_args()
    collect(args.device, {
        protocol.Status: logging_handler,
        protocol.Elec: elec_handler,
        protocol.TempHumidity: temp_humidity_handler,
        '*': logging_handler,
    })
