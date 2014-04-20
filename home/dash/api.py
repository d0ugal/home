from functools import wraps

from flask import Blueprint, request, jsonify, abort
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from home.ts import graph
from home.ts.models import Area, Device, Series, DataPoint, DeviceSeries

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


class ValuesResource(Resource):
    model = DataPoint


class AreasResource(Resource):
    model = Area


class GraphResource(ValuesResource):

    @kwarg_json_query
    def post(self, query=None):

        graph_func = None
        device_series_id = None

        if query is None:
            abort(400)

        qs = DataPoint.query.order_by(DataPoint.created_at.desc())

        if 'device_id' in query and 'series_id' in query:

            ds = DeviceSeries.query.filter_by(
                device_id=query['device_id'],
                series_id=query['series_id'],
            ).first()

            if 'graph' not in query:
                graph_func = graph.get_method(ds.series.graph)

            if ds is not None:
                device_series_id = ds.id

        if 'device_series_id' in query:
            device_series_id = query['device_series_id']

        if device_series_id is not None:
            qs = qs.filter_by(device_series_id=device_series_id)

        if 'start' in query and 'end' in query:
            start = query['start']
            end = query['end']
            qs = qs.filter(DataPoint.created_at.between(start, end))

        qs = qs.limit(10000)

        if graph_func is not None:
            qs = graph_func(qs)
        else:
            qs = [qs, ]

        return self.jsonify_qs(qs)


register_api(AreasResource, 'areas', '/areas/')
register_api(DeviceSeriesResource, 'device_series', '/device_series/')
register_api(DevicesResource, 'devices', '/devices/')
register_api(GraphResource, 'graph', '/graph/')
register_api(SeriesResource, 'series', '/series/')
register_api(ValuesResource, 'values', '/values/')
