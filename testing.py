from home.ts import *

Base.metadata.drop_all(engine)

syncdb()

s = Session()

get_series(s, 'test')
ser = get_series(s, 'test2')

dev = get_device(s, 1, 2, '3')

record(s, ser, dev, 100)

from home.report import *

run()
