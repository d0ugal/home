from flask import render_template, Blueprint

from home.ts.models import db, Device


web = Blueprint('Dashboard Web', __name__)


@web.route('/')
def dashboard():

    device_series = db.engine.execute(
        """ SELECT
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
            JOIN series ON series.id = device_series.series_id;
        """
    )

    structured = {}

    for row in device_series:

        structured[row.device_name] = structured.get(row.device_name, [])

        structured[row.device_name].append({
            'name': row.series_name,
            'value': row.latest_value,
            'created_at': row.latest_created_at,
        })

    return render_template('dashboard.html', devices=structured)


@web.route('/device/<device_name>/')
def device(device_name):

    device = Device.query.filter_by(name=device_name).first()

    return render_template('device.html', device=device)
