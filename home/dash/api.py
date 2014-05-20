"""
home.dash.api
=============

The web API that is primarilly used by the front end for rending graphs.
"""

from functools import wraps
from datetime import datetime

from flask import Blueprint, request, jsonify, abort
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from home import redis_series
from home.ts import graph
from home.ts.models import Area, Device, Series, DeviceSeries

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


def kwarg_json_query(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            json = request.get_json(force=True)
        except BadRequest:
            json = {}

        if isinstance(json, dict):
            kwargs['query'] = json
        else:
            raise Exception("Invalid JSON")

        return f(*args, **kwargs)

    return wrapper


class JSONResource(MethodView):

    def jsonify_qs(self, result_sets, **kwargs):

        r = []

        for result_set in result_sets:
            r.append({
                'values': [i.as_dict() for i in result_set],
                'count': len(list(result_set)),
            })

        return jsonify(data=r, **kwargs)


class Resource(JSONResource):

    page_size = 1000

    def get(self, resource_id=None, name=None):

        if resource_id is not None:
            resource = self.model.query.filter_by(id=resource_id).first()
            if not resource:
                abort(404)
            return jsonify(resource.as_dict())

        if name is not None:
            resource = self.model.query.filter_by(name=name).first()
            return jsonify(resource.as_dict())

        page = max(int(request.args.get('page', '0')), 1)

        results = self.model.query.order_by(
            self.model.created_at.desc())
        offset = (page - 1) * self.page_size
        results = results.limit(self.page_size).offset(offset)
        return self.jsonify_qs([results, ], page=page)


class DevicesResource(Resource):
    model = Device


class SeriesResource(Resource):
    model = Series


class DeviceSeriesResource(Resource):
    model = DeviceSeries


class AreasResource(Resource):
    model = Area


class GraphResource(JSONResource):

    def get(self, resource_id=None, name=None):
        abort(404)

    @kwarg_json_query
    def post(self, query=None):

        graph_func = None

        if query is None or len(query) == 0:
            abort(400)

        device_id, series_id = query['device_id'], query['series_id']

        key = "D-{0}:S-{1}".format(device_id, series_id)

        start = datetime.strptime(query['start'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(query['end'], "%Y-%m-%d %H:%M:%S")

        result_set = redis_series.query(key, start, end, 'hourly')

        if 'graph' not in query:
            ds = DeviceSeries.query.filter_by(
                device_id=device_id,
                series_id=series_id,
            ).first()
            graph_func = graph.get_method(ds.series.graph)

        if graph_func is not None:
            results = graph_func(result_set)
        else:
            results = {'full': result_set}

        return jsonify({
            'data': {
                'results': results
            }
        })


register_api(AreasResource, 'areas', '/areas/')
register_api(DeviceSeriesResource, 'device_series', '/device_series/')
register_api(DevicesResource, 'devices', '/devices/')
register_api(GraphResource, 'graph', '/graph/')
register_api(SeriesResource, 'series', '/series/')
