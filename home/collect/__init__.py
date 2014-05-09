"""
home.collect.__init__
=====================

A set of bound handlers which make the connection between the names returned
by python-rfxcom and the time series they should be inserted into.
"""

from home.collect.handlers import RecordingHandler, LoggingHandler


elec_handler = RecordingHandler({
    'current watts': 'current_watts',
    'total watts': 'total_watts'
})

temp_humidity_handler = RecordingHandler({
    'temperature': 'temperature',
    'humidity': 'humidity'
})

logging_handler = LoggingHandler()
