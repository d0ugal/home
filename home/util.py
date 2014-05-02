"""
home.util
=========

The random file all projects have where they dump stuff they don't know where
else to place.
"""


def get_or_create(model, **kwargs):

    from home import db

    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        return instance
