from datetime import datetime

from tests.base import BaseTestCase

from home.ts.models import Series, Device, DataPoint


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

        self.device = Device(82, 1, '0xAAAA', name="Test device")
        self.insert(self.device)

    def test_repr(self):

        repr(self.device)


class DataPointModelTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        now = datetime.now()

        self.series = Series(name="series_a")
        self.device = Device(82, 1, '0xAAAA', name="device_a")
        self.data_point = DataPoint(
            self.series, self.device, 10, created_at=now)

        self.insert(self.device)
        self.insert(self.series)
        self.insert(self.data_point)

    def test_repr(self):

        repr(self.data_point)

    def test_record(self):

        DataPoint.record(self.series, self.device, 100)
