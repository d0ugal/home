from datetime import datetime, timedelta
from random import randint

from home.ts import (Base, engine, syncdb, get_series, get_device, Session,
                     record)

Base.metadata.drop_all(engine)

syncdb()

s = Session()

ts1 = get_series(s, 'temperature')
ts2 = get_series(s, 'humidity')
ts3 = get_series(s, 'electricity')
ts4 = get_series(s, 'total_watts')

dev1 = get_device(s, 1, 2, '3', name='study')
dev2 = get_device(s, 2, 3, '4', name='kitchen')
dev3 = get_device(s, 3, 4, '5', name='electricity')

start = datetime.now()

watts = 1200000

for i in range(2000):

    d = start - timedelta(minutes=(i * 5) + randint(0, 30))

    if i % 100 == 0:
        print(d, i)

    record(s, ts1, dev1, randint(15, 30), created_at=d)
    record(s, ts2, dev1, randint(40, 60), created_at=d)

    record(s, ts1, dev2, randint(15, 30), created_at=d)
    record(s, ts2, dev2, randint(40, 60), created_at=d)

    record(s, ts3, dev3, randint(300, 6000), created_at=d)

    watts -= randint(300, 600)
    record(s, ts4, dev3, watts, created_at=d)
