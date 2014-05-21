"""
home.collect.handlers
=====================

Handlers are defined to handle events that Home collects. They will either
just record the event, or store it in a particular way or take action based on
the event.
"""

from logging import getLogger

from home import db
from home.exceptions import HandlerConfigError
from home.ts.models import Device, Series, DataPoint


def importer(dotted_path):
    module, object_ = dotted_path.rsplit('.', 1)
    try:
        mod = __import__(module, fromlist=[object_, ])
    except ImportError as e:
        raise ImportError("Failed to load {0}".format(dotted_path)) from e
    return getattr(mod, object_)


def load_handlers(handler_mapping):
    """
    Given a dictionary mapping which looks like the following, import the
    objects based on the dotted path and yield the packet type and handler as
    pairs.

    If the special string '*' is passed, don't process that, pass it on as it
    is a wildcard.

    If an non-string object is given for either packet or handler (key or
    value) assume these are the objects to use and yield them.

    ::
        {
        'rfxcom.protocol.Status': 'home.collect.logging_handler',
        'rfxcom.protocol.Elec': 'home.collect.elec_handler',
        'rfxcom.protocol.TempHumidity': 'home.collect.temp_humidity_handler',
        '*': 'home.collect.logging_handler'
        }
    """

    handlers = {}

    for packet_type, handler in handler_mapping.items():

        if packet_type == '*':
            Packet = packet_type
        elif isinstance(packet_type, str):
            Packet = importer(packet_type)
        else:
            Packet = packet_type

        if isinstance(handler, str):
            Handler = importer(handler)
        else:
            Handler = handler

        if Packet in handlers:
            raise HandlerConfigError(
                "Handler already provided for packet %s" % Packet)

        handlers[Packet] = Handler

    return handlers


class BaseHandler:

    def __init__(self):

        self.log = getLogger('home.collect.%s' % self.__class__.__name__)

    def format_packet(self, pkt):

        return " ".join("0x{0:02x}".format(x) for x in pkt)


class LoggingHandler(BaseHandler):

    def __call__(self, packet):

        self.log.warning(
            "Ignoring packet: {0} ({1})".format(
                packet, self.format_packet(packet.raw)))


class RecordingHandler(BaseHandler):

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
            self.log.info("ID=%s, %s=%s, Device ID=%s, Series ID=%s" % (
                id_, series_name, val, device.id, series.id))
            DataPoint.record(series, device, val)

        db.session.commit()
