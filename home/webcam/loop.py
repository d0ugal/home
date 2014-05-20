"""
home.webcam.loop
=================

"""

from asyncio import get_event_loop, coroutine, sleep
from logging import getLogger
from os.path import join

from aiohttp import request

from home import config
from home.webcam.models import Webcam


logger = getLogger('home.webcam.loop')


@coroutine
def fetch_urls():

    while True:

        for webcam in Webcam.query.all():
            logger.info("Fetching: %s " % (webcam.url, ))
            response = yield from request('GET', webcam.url)
            body = yield from response.read_and_close(decode=True)
            logger.info("Saving %s to %s" % (webcam.url, webcam.full_path))

            filename = join(config.MEDIA_FOLDER, webcam.filename)
            with open(filename,  'wb') as f:
                f.write(body)

        yield from sleep(10)


def collect(dev_name=None, callbacks=None):

    loop = get_event_loop()

    try:
        loop.run_until_complete(fetch_urls())
    finally:
        loop.close()
