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

        start = self.start.strftime("%Y-%m-%d %H:%M")
        end = self.end.strftime("%Y-%m-%d %H:%M")
        collections = []

        query2 = text("""SELECT data_point.created_at as date, data_point.value
        FROM data_point
        WHERE data_point.created_at >
        to_timestamp(:start, 'YYYY-MM-DD HH24:SS')
        AND data_point.created_at < to_timestamp(:end, 'YYYY-MM-DD HH24:SS')
        AND series_id = :series_id AND device_id = 1
        ORDER BY data_point.created_at ASC
        """)

        r2 = engine.execute(query2, start=start, end=end,
                            series_id=self.series.id)

        r2 = list(map(dict, r2.fetchall()))

        if r2:
            collections.append({
                'color': 'black',
                'name': 'Values',
                'renderer': 'scatterplot',
                'data': [{'x': o['date'], 'y': o['value']} for o in r2],
                'max': max(o['value'] for o in r2),
                'min': min(o['value'] for o in r2)
            })

        query = text("""SELECT
            coalesce(series_name) AS series_name,
            date,
            coalesce(min_v,0) AS min_v,
            coalesce(avg_v,0) AS avg_v,
            coalesce(max_v,0) AS max_v
        FROM
         generate_series(
            to_timestamp(:start, 'YYYY-MM-DD HH24:SS'),
            to_timestamp(:end, 'YYYY-MM-DD HH24:SS'),
            '1 hour') AS date
        LEFT OUTER JOIN
          (SELECT
                series.name AS series_name,
                date_trunc('hour', data_point.created_at) as day,
                min(data_point.value) as min_v,
                avg(data_point.value) as avg_v,
                max(data_point.value) as max_v
            FROM data_point
            JOIN series ON (series.id = data_point.series_id)
            AND series_id = :series_id AND device_id = 1
            GROUP BY series_id,
                series.name, day
            ORDER BY day
            ) results
        ON (date = results.day);
        """)

        r = engine.execute(query, start=start, end=end,
                           series_id=self.series.id)

        r = list(map(dict, r.fetchall()))

        if not r:
            return collections

        for collection in ['avg_v', ]:

            if collection == 'min_v':
                c = 'green'
            if collection == 'avg_v':
                c = 'orange'
            if collection == 'max_v':
                c = 'red'

            collections.append({
                'color': c,
                'name': collection,
                'renderer': 'line',
                'data': [{'x': o['date'], 'y': o[collection]} for o in r],
                'max': max(o[collection] for o in r),
                'min': min(o[collection] for o in r)
            })

        return collections
