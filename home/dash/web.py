from collections import OrderedDict

from sqlalchemy.sql import text
from flask import render_template, Blueprint

from home.ts.models import db, Area, Device, Series


web = Blueprint('Dashboard Web', __name__)


@web.context_processor
def inject_devices():
    return dict(devices=Device.query.join(Area).order_by(Area.name).all())


@web.route('/')
@web.route('/areas/<device_name>/')
def dashboard(device_name=None):

    series_map = {s.id: s for s in Series.query.all()}

    query = """ SELECT
    device.id as device_id, area.name as device_name,
    series.id as series_id, series.name as series_name,
    ARRAY (
        SELECT hstore(data_point)
        FROM data_point
        WHERE data_point.device_series_id = device_series.id
        ORDER BY data_point.created_at DESC
        LIMIT 30
    ) as latest
    FROM device_series
    JOIN device ON device.id = device_series.device_id
    JOIN series ON series.id = device_series.series_id
    JOIN area ON area.id = device.area_id"""

    if device_name:
        kwargs = {'device_name': device_name}
        query += "\n    WHERE area.name = :device_name"
    else:
        kwargs = {}

    query += "\n    ORDER BY series_name, device_name"

    device_series = db.engine.execute(text(query), **kwargs)

    structured = OrderedDict()

    for row in device_series:

        structured[row.device_name] = structured.get(row.device_name, [])

        structured[row.device_name].append({
            'series_id': row.series_id,
            'model': series_map[row.series_id],
            'device_id': row.device_id,
            'name': row.series_name,
            'value': row.latest[0]['value'],
            'created_at': row.latest[0]['created_at'],
            'data_points': row.latest,
            'sparkline': ','.join(reversed([d['value'] for d in row.latest]))
        })

    if device_name is not None:
        template = 'device.html'
    else:
        template = 'dashboard.html'

    return render_template(
        template,
        device_readings=structured,
        device_name=device_name,
    )
