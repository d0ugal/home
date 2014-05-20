"""
home.ts.redis
=============


series:device:YYYY-MM-DD-HH-MM-SS

current watts:1:2014-05-19-20-45-49

"""

from datetime import datetime
from decimal import Decimal
from itertools import chain

from dateutil.relativedelta import relativedelta
from redis import StrictRedis


RESOLUTIONS = {
    # 'minute': ("%Y-%m-%dT%H:%M", relativedelta(minutes=1)),
    'hourly': ("%Y-%m-%dT%H", relativedelta(hours=1)),
    'daily': ("%Y-%m-%d", relativedelta(days=1)),
    # 'monthly': ("%Y-%m", relativedelta(months=1)),
}

EXPIRE_AFTER = 60 * 60 * 24 * 7  # 7 days in seconds


class RedisSeries:

    def __init__(self, host=None, port=None, db=None, password=None):

        self._redis = StrictRedis(decode_responses=True)

    def push(self, series, value, dt=None):

        pipeline = self._redis.pipeline()

        if dt is None:
            dt = datetime.utcnow()

        timestamp = dt.isoformat()

        recent_key = self.named_key(series, "recent")

        pipeline.lpush(recent_key, value)
        pipeline.ltrim(recent_key, 0, 60)
        pipeline.sadd("series", series)
        pipeline.hset("latest", series, value)
        pipeline.hset("updated", series, timestamp)

        for resolution, (dt_fmt, delta) in RESOLUTIONS.items():

            key = self.event_key(series, dt, dt_fmt)
            pipeline.hset(key, timestamp, value)
            pipeline.expire(key, EXPIRE_AFTER)

        pipeline.execute()

    def event_key(self, series, dt, dt_fmt):
        return "{0}:{1}".format(series, dt.strftime(dt_fmt))

    def named_key(self, series, name):
        return "{0}:{1}".format(series, name)

    def query(self, series, start, end, resolution):

        dt_fmt, delta = RESOLUTIONS[resolution]
        current = start
        pipeline = self._redis.pipeline()

        while current < end:
            key = self.event_key(series, current, dt_fmt)
            pipeline.hgetall(key)
            current += delta

        results = pipeline.execute()

        results = sorted(list(chain(*[result.items() for result in results])))

        return [(r[0], Decimal(r[1])) for r in results]

    def status(self):

        pipeline = self._redis.pipeline()

        pipeline.hgetall("latest")
        pipeline.hgetall("updated")

        return pipeline.execute()

    def latest(self, series):

        return self._redis.lrange(self.named_key(series, "recent"), 0, -1)
