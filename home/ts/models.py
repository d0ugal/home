from datetime import datetime

from sqlalchemy import (Column, Numeric, Integer, String, ForeignKey, DateTime,
                        UniqueConstraint, Text)
from sqlalchemy.orm import relationship, backref
from flask.ext.sqlalchemy import SQLAlchemy

from home.util import get_or_create

db = SQLAlchemy()


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

    device_series = relationship(
        "DeviceSeries", order_by=created_at.desc(),
        backref=backref('data_points'))

    def __init__(self, device_series, value, created_at=None):
        self.created_at = datetime.utcnow()
        super().__init__()
        self.device_series = device_series
        self.value = value
        self.created_at = created_at

    @classmethod
    def record(cls, series, device, value, created_at=None):
        ds = DeviceSeries.get_or_create(device=device, series=series)
        data_point = DataPoint(device_series=ds, value=value)
        if created_at is None:
            data_point.created_at = datetime.utcnow()
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

    device = relationship(
        "Device", backref=backref('device_series'), lazy='joined')
    series = relationship(
        "Series", backref=backref('device_series'), lazy='joined')

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

    graph = relationship(
        "Graph", backref=backref('series'), lazy='joined', uselist=False)

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

    area = relationship(
        "Area", backref=backref('devices'), lazy='joined', uselist=False)

    series = relationship(
        "Series",
        secondary=("join(DeviceSeries, Series, DeviceSeries.series_id == "
                   "Series.id)"),
        primaryjoin=("and_(Device.id == DeviceSeries.device_id, Series.id == "
                     "DeviceSeries.series_id)"),
        secondaryjoin="Series.id == DeviceSeries.series_id"
    )

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
