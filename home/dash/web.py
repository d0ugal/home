from datetime import datetime

from flask import render_template, jsonify, Blueprint

from home.ts import SeriesGenerator
from home.ts.models import DataPoint, Device, Series


web = Blueprint('Dashboard Web', __name__)


@web.route('/')
def dashboard():

    devices = Device.query\
        .join(DataPoint)\
        .join(Series)\
        .order_by(Device.name)\
        .all()

    return render_template('dashboard.html', devices=devices)
