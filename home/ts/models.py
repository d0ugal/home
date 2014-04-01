from datetime import datetime

from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from flask.ext.sqlalchemy import SQLAlchemy

from home.util import get_or_create

db = SQLAlchemy()


class SerialiseMixin:

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Series(db.Model, SerialiseMixin):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String(20), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.name = name

    @classmethod
    def get_or_create(cls, **kwargs):
        r = get_or_create(cls, **kwargs)
        return r

    def __repr__(self):
        return "Series(name=%r)" % (self.name)


class Device(db.Model, SerialiseMixin):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String(20), nullable=True, unique=True)
    device_type = Column(Integer)
    device_sub_type = Column(Integer)
    device_id = Column(String(20), nullable=False, unique=True)

    def __init__(self, device_type, device_sub_type, device_id, name=None):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.device_type = device_type
        self.device_sub_type = device_sub_type
        self.device_id = device_id
        self.name = name

    def as_dict(self):

        d = super().as_dict()

        latest = {}

        for series in self.get_series():

            series_latest = (
                DataPoint.query
                .filter_by(device=self, series=series)
                .order_by(DataPoint.created_at.desc())
                .first()
            )
            latest[series.name] = SerialiseMixin.as_dict(series_latest)

        d['latest'] = latest

        return d

    def get_series(self):
        return Series.query.join(DataPoint).filter_by(device=self).all()

    @classmethod
    def get_or_create(cls, device_type, device_sub_type, device_id):
        return get_or_create(cls, device_type=device_type,
                             device_sub_type=device_sub_type,
                             device_id=device_id)

    def __repr__(self):
        return "Device(name=%s, ID=%r)" % (
            self.name, self.device_id)


class DataPoint(db.Model, SerialiseMixin):
    __tablename__ = 'data_point'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    value = Column(Numeric, nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'))
    device_id = Column(Integer, ForeignKey('device.id'))

    series = relationship("Series",
                          backref=backref('data_points', order_by=id))
    device = relationship("Device",
                          backref=backref('data_points', order_by=id))

    def __init__(self, series, device, value, created_at=None):
        self.created_at = datetime.utcnow()
        super().__init__()
        self.series = series
        self.device = device
        self.value = value
        self.created_at = created_at

    @classmethod
    def record(cls, series, device, value, created_at=None):
        data_point = DataPoint(series=series, device=device, value=value)
        if created_at is None:
            data_point.created_at = datetime.utcnow()
        db.session.add(data_point)
        return data_point

    def as_dict(self):

        d = super().as_dict()
        d['device'] = self.device.as_dict()
        d['series'] = self.series.as_dict()

        return d

    def __repr__(self):
        return "<Data Point(%s, %s, value=%s, created_at=%s)>" % (
            self.series, self.device, self.value, self.created_at)
