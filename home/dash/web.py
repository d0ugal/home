from sqlalchemy.sql import text
from flask import render_template, Blueprint

from home.ts.models import db, Device


web = Blueprint('Dashboard Web', __name__)


@web.context_processor
def inject_devices():
    return dict(devices=Device.query.all())


@web.route('/')
@web.route('/device/<device_name>/')
def dashboard(device_name=None):

    query = """ SELECT
        device.id as device_id, device.name as device_name,
        series.id as series_id, series.name as series_name,
        (
            SELECT data_point.value
            FROM data_point
            WHERE data_point.device_series_id = device_series.id
            ORDER BY data_point.created_at DESC
            LIMIT 1
        ) AS latest_value,
        (
            SELECT data_point.created_at
            FROM data_point
            WHERE data_point.device_series_id = device_series.id
            ORDER BY data_point.created_at DESC
            LIMIT 1
        ) AS latest_created_at
    FROM device_series
    JOIN device ON device.id = device_series.device_id
    JOIN series ON series.id = device_series.series_id
    """

    if device_name:
        kwargs = {'device_name': device_name}
        query += "WHERE device.name = :device_name"
    else:
        kwargs = {}

    device_series = db.engine.execute(text(query), **kwargs)

    structured = {}

    for row in device_series:

        structured[row.device_name] = structured.get(row.device_name, [])

        structured[row.device_name].append({
            'series_id': row.series_id,
            'device_id': row.device_id,
            'name': row.series_name,
            'value': row.latest_value,
            'created_at': row.latest_created_at,
        })

    if device_name is not None:
        template = 'device.html'
    else:
        template = 'dashboard.html'

    return render_template(
        template,
        device_readings=structured,
        device_name=device_name
    )
