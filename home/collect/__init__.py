from home import app
from home.collect.handlers import RecordingHander, LoggingHandler
from home.collect.loop import collect


elec_handler = RecordingHander({
    'current watts': 'current_watts',
    'total watts': 'total_watts'
})

temp_humidity_handler = RecordingHander({
    'temperature': 'temperature',
    'humidity': 'humidity'
})

logging_handler = LoggingHandler()


def run(device):

    with app.app_context():
        collect(device)
