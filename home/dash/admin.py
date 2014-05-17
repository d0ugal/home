"""
home.dash.admin
==================

"""

from flask import flash
from flask.ext.admin.actions import action
from flask.ext.admin.babel import lazy_gettext
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.tools import get_query_for_ids
from flask.ext.login import current_user

from home import db
from home.dash.models import User
from home.ts.models import Graph, Series, Device, DeviceSeries, Area
from home.webcam.models import Webcam


class AuthedModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()


class DeviceModelView(AuthedModelView):

    @action('merge',
            lazy_gettext('Merged into newest'),
            lazy_gettext("Are you sure you want to merged these devices into "
                         "the most recently created?"))
    def merge(self, ids):

        if len(ids) > 2:
            flash("Only two devices can be merged at a time.")
            return

        query = get_query_for_ids(self.get_query(), self.model, ids)

        devices = query.order_by(Device.created_at).all()

        types = set(device.device_type for device in devices)
        sub_types = set(device.device_sub_type for device in devices)

        if len(types) > 1 or len(sub_types) > 1:
            flash("Devices of different types or different sub types can't be "
                  "automatically merged.")
            return

        old_device, new_device = query

        if new_device.area is None:
            new_device.area = old_device.area

        for new_device_series in new_device.device_series:

            old_device_series = DeviceSeries.query.filter(
                DeviceSeries.series_id == new_device_series.series_id,
                DeviceSeries.device_id == old_device.id,
            ).one()

            flash("%r - %r " % (new_device_series, old_device_series))

            flash("%r" % old_device_series.data_points)

        db.session.commit()


def setup_admin(admin):

    admin.add_view(AuthedModelView(Area, db.session))
    admin.add_view(DeviceModelView(Device, db.session))
    admin.add_view(AuthedModelView(Series, db.session))
    admin.add_view(AuthedModelView(DeviceSeries, db.session))
    admin.add_view(AuthedModelView(Graph, db.session))

    admin.add_view(AuthedModelView(User, db.session))

    admin.add_view(AuthedModelView(Webcam, db.session))
