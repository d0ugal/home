from unittest.mock import Mock

from home.collect.handlers import RecordingHander
from home import app


def run():
    r = RecordingHander({
        'series_name2': 'value_name2',
        'series_name4': 'packet_type'
    })

    p = Mock()
    p.data = {
        'value_name2': 70,
        'packet_type': 33,
        'sub_type': 1,
        'id': 'test',
    }

    r(p)


with app.app_context():
    run()
