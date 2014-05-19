"""
home.ts.models
==============

A set of models for storing data points for a time series and device. These
can then also be attributed to an Area, which typically defines a room in the
house.
"""

from datetime import datetime

from sqlalchemy import (Column, Numeric, Integer, String, ForeignKey, DateTime,
                        UniqueConstraint, Text)

from home import db
from home.util import get_or_create
from home import redis_series


class SerialiseMixin:

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DataPoint(db.Model, SerialiseMixin):
    __tablename__ = 'data_point'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True)
    value = Column(Numeric, nullable=False, index=True)
    device_series_id = Column(Integer, ForeignKey('device_series.id'),
                              index=True, nullable=False)

    device_series = db.relationship(
        "DeviceSeries", order_by=created_at.desc(),
        backref=db.backref('data_points'))

    def __init__(self, device_series, value, created_at=None):
        self.created_at = datetime.utcnow()
        super().__init__()
        self.device_series = device_series
        self.value = value
        self.created_at = created_at

    def push_to_redis(self):

        ds = self.device_series
        key = "D-%s:S-%s" % (ds.device_id, ds.series_id)
        redis_series.push(key, self.value, self.created_at)

    @classmethod
    def record(cls, series, device, value, created_at=None):
        ds = DeviceSeries.get_or_create(device=device, series=series)
        data_point = DataPoint(device_series=ds, value=value)
        if created_at is None:
            data_point.created_at = datetime.utcnow()
        data_point.push_to_redis()
        db.session.add(data_point)
        return data_point

    def __repr__(self):
        return "<Data Point(%s, value=%s, created_at=%s)>" % (
            self.device_series, self.value, self.created_at)


class DeviceSeries(db.Model, SerialiseMixin):
    __tablename__ = 'device_series'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)

    device = db.relationship(
        "Device", backref=db.backref('device_series'), lazy='joined')
    series = db.relationship(
        "Series", backref=db.backref('device_series'), lazy='joined')

    __table_args__ = (
        UniqueConstraint('series_id', 'device_id', name='_series_device_uc'),
    )

    def __init__(self, device, series):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.series = series
        self.device = device

    @property
    def latest_reading(self):
        return DataPoint.query\
            .filter_by(device_series=self)\
            .order_by(DataPoint.created_at.desc())\
            .limit(1).first()

    @classmethod
    def get_or_create(cls, **kwargs):
        return get_or_create(cls, **kwargs)

    def __repr__(self):
        return "DeviceSeries(device_id=%s, series_id=%s)" % (
            self.device_id, self.series_id)


class Graph(db.Model, SerialiseMixin):

    __tablename__ = 'graph'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, index=True, unique=True)
    description = Column(Text)
    aggregator = Column(String(20), nullable=False)

    def __repr__(self):
        return "Graph(name=%s)" % (self.name, )


class Series(db.Model, SerialiseMixin):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, index=True, nullable=False)
    name = Column(String(20), nullable=False, index=True, unique=True)
    graph_id = Column(Integer, ForeignKey('graph.id'))

    graph = db.relationship(
        "Graph", backref=db.backref('series'), lazy='joined', uselist=False)

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


class Area(db.Model, SerialiseMixin):
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, index=True, nullable=False)
    name = Column(String(20), nullable=True, index=True, unique=True)

    def __init__(self, name):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.name = name

    def __repr__(self):
        return "Area(name=%r)" % (self.name)


class Device(db.Model, SerialiseMixin):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, index=True, nullable=False)
    device_type = Column(Integer, index=True)
    device_sub_type = Column(Integer, index=True)
    device_id = Column(String(20), nullable=False, unique=True)
    area_id = Column(Integer, ForeignKey('area.id'))

    area = db.relationship(
        "Area", backref=db.backref('devices'), lazy='joined', uselist=False)

    def __init__(self, device_type, device_sub_type, device_id, area=None):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.device_type = device_type
        self.device_sub_type = device_sub_type
        self.device_id = device_id
        self.area = area

    @classmethod
    def get_or_create(cls, device_type, device_sub_type, device_id):
        return get_or_create(cls, device_type=device_type,
                             device_sub_type=device_sub_type,
                             device_id=device_id)

    def __repr__(self):
        return "Device(name=%s, ID=%r)" % (
            self.area, self.device_id)
