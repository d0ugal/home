"""
home.collect.loop
=================

The basic event loop used by Home for running the python-rfxcom integration.
"""

from asyncio import get_event_loop
from logging import getLogger

from rfxcom.transport import AsyncioTransport

from home import config
from home.collect.handlers import load_handlers


logger = getLogger('home.collect.loop')


def collect(dev_name=None, callbacks=None):

    if callbacks is None:
        callbacks = dict(load_handlers(config.PACKET_HANDLERS))

    loop = get_event_loop()

    try:
        logger.info("Starting collection from:", dev_name)
        AsyncioTransport(dev_name, loop, callbacks=callbacks)
        loop.run_forever()
    finally:
        loop.close()
