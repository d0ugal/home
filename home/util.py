"""
home.util
=========

The random file all projects have where they dump stuff they don't know where
else to place.
"""

from datetime import datetime
from contextlib import ContextDecorator
from time import clock


def get_or_create(model, **kwargs):

    from home import db

    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        return instance


def dtparse(string):

    date_formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    )

    for date_format in date_formats:

        return datetime.strptime(string, date_format)


class timer(ContextDecorator):

    def __init__(self, name, log=None):
        self.name = name
        self.interval = None
        self.log = log

    def __enter__(self):
        self.start = clock()
        return self

    def __exit__(self, *args):
        self.end = clock()
        self.interval = self.end - self.start

        if self.log is not None:
            self.log.debug(str(self))

    def __str__(self):
        return "{} took {:.2}s".format(self.name, self.interval)
