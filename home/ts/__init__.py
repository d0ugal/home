from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from .models import Base, Series, Device, DataPoint

engine = create_engine('postgresql://home:home@localhost:5432/home')
Session = sessionmaker(bind=engine)


def syncdb():

    Base.metadata.create_all(engine)


def get_series(session, name):
    series = Series.get_or_create(session, name=name)
    session.commit()
    return series


def get_device(session, device_type, device_sub_type, device_id, name=None):
    device = Device.get_or_create(session, device_type=device_type,
                                  device_sub_type=device_sub_type,
                                  device_id=device_id, name=name)
    session.commit()
    return device


def record(session, series, device, value, created_at=None):
    data_point = DataPoint(series=series, device=device, value=value,
                           created_at=created_at)
    session.add(data_point)
    session.commit()
    return data_point


class SeriesGenerator:

    def __init__(self, series_name, start, end):

        self.session = Session()

        self.series = Series.get(self.session, name=series_name)

        self.start = start
        self.end = end

    def all(self):

        query = text("""SELECT
            coalesce(device_id) AS device_id,
            coalesce(device_name) AS device_name,
            coalesce(series_id) AS series_id,
            coalesce(series_name) AS series_name,
            date,
            coalesce(min_v,0) AS min_v,
            coalesce(max_v,0) AS max_v,
            coalesce(avg_v,0) AS avg_v,
            coalesce(stddev_v,0) AS stddev_v
        FROM
         generate_series(
            to_timestamp(:start, 'YYYY-MM-DD HH24:SS'),
            to_timestamp(:end, 'YYYY-MM-DD HH24:SS'),
            '1 hour') AS date
        LEFT OUTER JOIN
          (SELECT
                data_point.device_id,
                device.name AS device_name,
                series_id,
                series.name AS series_name,
                date_trunc('hour', data_point.created_at) as day,
                min(data_point.value) as min_v,
                max(data_point.value) as max_v,
                avg(data_point.value) as avg_v,
                stddev(data_point.value) as stddev_v
            FROM data_point
            JOIN series ON (series.id = data_point.series_id)
            JOIN device ON (device.id = data_point.device_id)
            AND series_id = :series_id
            GROUP BY data_point.device_id, device.name, series_id,
                series.name, day
            ) results
        ON (date = results.day);
        """)

        start = self.start.strftime("%Y-%m-%d %H:%M")
        end = self.end.strftime("%Y-%m-%d %H:%M")

        r = engine.execute(query, start=start, end=end,
                           series_id=self.series.id)

        r = list(map(dict, r.fetchall()))

        collections = []

        for collection in ['min_v', 'max_v', 'avg_v', 'stddev_v']:

            collections.append({
                'name': collection,
                'data': [{'x': o['date'], 'y': o[collection]} for o in r]
            })

        return collections
