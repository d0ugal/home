from logging import getLogger

from home.ts.models import Device, Series, DataPoint
from home import db


class BaseHandler:

    def __init__(self):

        self.log = getLogger('home.collect.%s' % self.__class__.__name__)

    def format_packet(self, pkt):

        return " ".join("0x{0:02x}".format(x) for x in pkt)


class LoggingHandler(BaseHandler):

    def __call__(self, packet):

        self.log.warning(
            "Ignoring packet: {0}".format(self.format_packet(packet.raw)))


class RecordingHander(BaseHandler):

    def __init__(self, mapping):
        super().__init__()
        self.mapping = mapping

    def __call__(self, packet):

        device = Device.get_or_create(packet.data['packet_type'],
                                      packet.data['sub_type'],
                                      packet.data['id'])

        for series_name, value_name in self.mapping.items():

            series = Series.get_or_create(name=series_name)
            db.session.commit()
            try:
                val = packet.data[value_name]
            except KeyError:
                self.log.error("Failed to find %s in packet. Key list: %r" % (
                    value_name, sorted(packet.data.keys())))
                return

            id_ = packet.data.get('id')
            self.log.info("ID=%s, %s=%s" % (id_, series_name, val))
            DataPoint.record(series, device, val)

        db.session.commit()
