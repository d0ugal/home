"""
home.dash.web
=============

The web controllers for rendering login, logout and dashboard screens.
"""
from logging import getLogger

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user

from home import redis_series
from home.dash.models import User
from home.ts.models import Area, DeviceSeries, Device
from home.webcam.models import Webcam
from home.util import timer


web = Blueprint('Dashboard Web', __name__)
log = getLogger('home.dash.web')


@web.context_processor
@timer("Inject Areas", log)
def inject_areas():
    return {
        'areas': Area.query.order_by(Area.name).all(),
    }


@web.context_processor
@timer("Inject Webcams", log)
def inject_webcams():
    return dict(webcams=Webcam.query.all())


@web.route('/')
@web.route('/areas/<area_name>/')
@timer("Dashboard Render", log)
@login_required
def dashboard(area_name=None):

    device_series = DeviceSeries.query

    if area_name:
        device_series = device_series\
            .filter(Area.name == area_name)\
            .join(DeviceSeries.device)\
            .join(Device.area)\
            .order_by(Area.name)

    latest, updated = redis_series.status()

    device_series_values = []

    for ds in device_series:

        key = "D-{0}:S-{1}".format(ds.device_id, ds.series_id)

        latest_value = latest.get(key)
        updated_at = updated.get(key)
        latest_values = ",".join(redis_series.latest(key))

        line = (ds, latest_value, updated_at, latest_values)
        device_series_values.append(line)

    if area_name is not None:
        template = 'device.html'
    else:
        template = 'dashboard.html'

    return render_template(
        template,
        device_readings=device_series_values,
        area_name=area_name,
    )


@web.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    registered_user = User.query.filter_by(username=username).first()

    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('.login'))

    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('.login'))

    login_user(registered_user, remember=True)

    flash('Logged in successfully')

    return redirect(request.args.get('next') or url_for('.dashboard'))


@web.route('/logout/', methods=['GET', ])
def logout():
    logout_user()
    return redirect(url_for('.login'))
