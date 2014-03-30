from functools import wraps

from flask import Blueprint, request

from home.ts.models import Device, Series, DataPoint

api = Blueprint('Dashboard API', __name__)


def _kwargs_from_request(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        json = request.get_json(force=True)

        if isinstance(json, dict):
            kwargs.update(json)
        else:
            raise Exception("Invalid JSOn.")

        return f(*args, **kwargs)

    return wrapper


def register_url_rules(rules):

    for rule, function, methods in rules:
        api.add_url_rule(rule, view_func=function, methods=methods)


class Resource(object):

    def __init__(self, model, resource_name=None):
        self.model = model

        if resource_name is None:
            self.resource_name = self.model.__class__.__name__.lower()
        else:
            self.resource_name = resource_name

        register_url_rules(self.get_url_rules())

    @property
    def session(self):
        from home import db
        return db.session

    def get_url_rules(self):

        base = '/{0}/'.format(self.resource_name)
        id_ = '/{0}/<id>/'.format(self.resource_name)

        return (
            (base, self.get, ['GET', ]),
            (id_, self.get, ['GET', ]),
            (base, self.post, ['POST', ]),
            (id_, self.put, ['PUT', ]),
            (id_, self.delete, ['DELETE', ]),
        )

    def get(self, id_=None, **kwargs):

        if id_ is not None:
            return self.model.get(self.session, id_=id_)

        return self.model.filter_by(self.session, **kwargs)

    def post(self, **kwargs):
        instance = self.model.create(self.session, **kwargs)
        return instance

    def put(self, id_, **kwargs):
        instance = self.model.update(self.session, id_=id_, **kwargs)
        return instance

    def delete(self, id_):
        return self.model.delete(id_=id_)

devices = Resource(Device, "devices")
# series = Resource(Series, "series")
# data_points = Resource(DataPoint, "data_points")
