from sqlalchemy import func

from home import app, db
from home.ts.models import Series, DataPoint, Device


def report():

    print()

    series = Series.query.all()

    count, start, latest = db.session.query(
        func.count(DataPoint.value),
        func.min(DataPoint.created_at),
        func.max(DataPoint.created_at)
    ).one()

    print("Overall stats:")
    print("    Data Points :", count)
    print("    Data From   :", start)
    print("    Last Read   :", latest)
    print()

    for s in series:

        max_v, min_v, count, avg, start, latest = db.session.query(
            func.max(DataPoint.value),
            func.min(DataPoint.value),
            func.avg(DataPoint.value),
            func.count(DataPoint.value),
            func.min(DataPoint.created_at),
            func.max(DataPoint.created_at)
        ).filter_by(series=s).one()

        print("Metric:", s.name)
        print("    Data Points :", count)
        print("    Data From   :", start)
        print("    Last Read   :", latest)
        print("    Minimum     :", min_v)
        print("    Maximum     :", max_v)
        print("    Average     :", avg)

        print()
        print()

    print("Latest readings...")

    for device in Device.query.all():
        latest = DataPoint.query.filter_by(device=device).first().created_at
        print(latest.strftime("%Y-%m-%d %H:%M:%S"), device.name)

    print()
    print()


def run():

    with app.app_context():
        report()
