from datetime import datetime

from flask import render_template, jsonify, Blueprint

from home.ts import SeriesGenerator
from home.ts.models import DataPoint, Device


web = Blueprint('Dashboard Web', __name__)


@web.route('/')
def dashboard():

    devices = Device.query.join(DataPoint).order_by(DataPoint.series_id).all()

    return render_template('dashboard.html', devices=devices)


@web.route('/data/<series>/<device>/<start>/<end>/')
def range(series, device, start, end):

    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    generator = SeriesGenerator(series, device, start_dt, end_dt)

    return jsonify(
        series=generator.all()
    )
