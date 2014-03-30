from datetime import datetime

from flask import render_template, jsonify, Blueprint

from home.ts import SeriesGenerator
from home.ts.models import DataPoint, Series, Device


web = Blueprint('Dashboard Web', __name__)


@web.route('/')
def dashboard():
    return render_template('dashboard.html')


@web.route('/data/<series>/<device>/<start>/<end>/')
def range(series, device, start, end):

    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    generator = SeriesGenerator(series, device, start_dt, end_dt)

    return jsonify(
        series=generator.all()
    )


@web.route('/data/<series>/<device>/latest/')
def latest(series, device):

    from home import db

    data_point = db.session.query(DataPoint)\
        .join(Series).join(Device)\
        .filter(Series.name == series).filter(Device.name == device)\
        .order_by(DataPoint.created_at.desc()).first()

    return jsonify(
        **data_point.as_dict()
    )
