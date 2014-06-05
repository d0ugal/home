"""
home.util
=========

The random file all projects have where they dump stuff they don't know where
else to place.
"""

from datetime import datetime


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
