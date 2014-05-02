"""
home.collect.__init__
=====================

A set of bound handlers which make the connection between the names returned
by python-rfxcom and the time series they should be inserted into.
"""

from home.collect.handlers import RecordingHander, LoggingHandler


elec_handler = RecordingHander({
    'current watts': 'current_watts',
    'total watts': 'total_watts'
})

temp_humidity_handler = RecordingHander({
    'temperature': 'temperature',
    'humidity': 'humidity'
})

logging_handler = LoggingHandler()
