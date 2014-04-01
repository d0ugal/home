from functools import wraps

from flask import Blueprint, request, jsonify, abort
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from home.ts.models import Device, Series, DataPoint

api = Blueprint('Dashboard API', __name__)


def register_api(view, endpoint, url):
    view_func = view.as_view(endpoint)

    api.add_url_rule(url, defaults={'resource_id': None, 'name': None},
                     view_func=view_func, methods=['GET', ])

    api.add_url_rule(url, view_func=view_func, methods=['POST', ])

    api.add_url_rule('%s<int:resource_id>' % (url), defaults={'name': None},
                     view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

    api.add_url_rule('%s<string:name>' % (url), defaults={'resource_id': None},
                     view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def kwargs_from_request(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            json = request.get_json(force=True)
        except BadRequest:
            json = {}

        if isinstance(json, dict):
            kwargs.update(json)
        else:
            raise Exception("Invalid JSON")

        return f(*args, **kwargs)

    return wrapper


class Resource(MethodView):

    page_size = 100

    def jsonify_qs(self, qs, **kwargs):
        return jsonify(results=[i.as_dict() for i in qs], **kwargs)

    @kwargs_from_request
    def get(self, resource_id=None, name=None, **kwargs):

        if resource_id is not None:
            resource = self.model.query.filter_by(id=resource_id).first()
            if not resource:
                abort(404)
            return jsonify(resource.as_dict())

        if name is not None:
            resource = self.model.query.filter_by(name=name).first()
            return jsonify(resource.as_dict())

        page = max(int(request.args.get('page', '0')), 1)

        results = self.model.query.filter_by(**kwargs)
        count = results.count()
        offset = (page - 1) * self.page_size
        results = results.limit(self.page_size).offset(offset)
        return self.jsonify_qs(results, count=count, page=page)


class DevicesResource(Resource):
    model = Device


class SeriesResource(Resource):
    model = Series


class ValuesResource(Resource):
    model = DataPoint


register_api(DevicesResource, 'devices', '/devices/')
register_api(SeriesResource, 'series', '/series/')
register_api(ValuesResource, 'values', '/values/')
