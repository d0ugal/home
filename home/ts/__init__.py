from sqlalchemy.sql import text

from home.ts.models import Series, Device


def filter_ints(series):

    for item in series:
        if item is not None and item > 0:
            yield item


class SeriesGenerator:

    def __init__(self, series_name, device_name, start, end):

        self.series = Series.query.filter_by(name=series_name).first()
        self.device = Device.query.filter_by(name=device_name).first()

        self.start = start
        self.end = end

    def all(self):

        from home import db
        start = self.start.strftime("%Y-%m-%d %H:%M")
        end = self.end.strftime("%Y-%m-%d %H:%M")
        collections = []

        query2 = text("""SELECT data_point.created_at as date, data_point.value
        FROM data_point
        WHERE data_point.created_at >
        to_timestamp(:start, 'YYYY-MM-DD HH24:SS')
        AND data_point.created_at < to_timestamp(:end, 'YYYY-MM-DD HH24:SS')
        AND series_id = :series_id AND device_id = :device_id
        ORDER BY data_point.created_at ASC
        """)

        r2 = db.engine.execute(query2, start=start, end=end,
                               series_id=self.series.id,
                               device_id=self.device.id)

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

        query = text("""SELECT series.name AS series_name,
            date_trunc('hour', data_point.created_at) as date,
            avg(data_point.value)
        FROM data_point
        JOIN series ON (series.id = data_point.series_id)
        WHERE data_point.created_at >
        to_timestamp(:start, 'YYYY-MM-DD HH24:SS')
        AND data_point.created_at < to_timestamp(:end, 'YYYY-MM-DD HH24:SS')
        AND series_id = :series_id AND device_id = :device_id
        GROUP BY series_id,
            series.name, date
        ORDER BY date;
        """)

        r = db.engine.execute(query, start=start, end=end,
                              series_id=self.series.id,
                              device_id=self.device.id)

        r = list(map(dict, r.fetchall()))

        if not r:
            return collections

        collections.append({
            'color': 'orange',
            'name': 'avg',
            'renderer': 'line',
            'data': [{'x': o['date'], 'y': o['avg']} for o in r],
            'max': max(filter_ints(o['avg'] for o in r)),
            'min': min(filter_ints(o['avg'] for o in r))
        })

        return collections
