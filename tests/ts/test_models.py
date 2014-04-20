from datetime import datetime

from tests.base import BaseTestCase

from home.ts.models import Area, Series, Device, DataPoint, DeviceSeries


class SeriesModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.series = Series(name="Series")
        self.insert(self.series)

    def test_repr(self):

        repr(self.series)


class DeviceModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.area = Area(name="livingroom")
        self.device = Device(82, 1, '0xAAAA', area=self.area)
        self.insert(self.device)

    def test_repr(self):

        repr(self.device)


class DataPointModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        now = datetime.now()

        self.series = Series(name="series_a")
        self.area = Area(name="livingroom")
        self.device = Device(82, 1, '0xAAAA', area=self.area)
        self.device_series = DeviceSeries(self.device, self.series)
        self.data_point = DataPoint(self.device_series, 10, created_at=now)

        self.insert(self.device)
        self.insert(self.series)
        self.insert(self.data_point)

    def test_repr(self):

        repr(self.data_point)

    def test_record(self):

        DataPoint.record(self.series, self.device, 100)
