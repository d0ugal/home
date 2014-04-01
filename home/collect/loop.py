from asyncio import get_event_loop

from rfxcom.transport import AsyncioTransport

from home.config import PACKET_HANDLERS
from home.collect.handlers import load_handlers


def collect(dev_name, callbacks=None):

    if callbacks is None:
        callbacks = dict(load_handlers(PACKET_HANDLERS))

    loop = get_event_loop()

    try:

        AsyncioTransport(dev_name, loop, callbacks=callbacks)
        loop.run_forever()

    finally:
        loop.close()
