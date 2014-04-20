from datetime import datetime

from tests.base import BaseTestCase

from home.ts.models import Area, Device, Series, DataPoint, DeviceSeries


class ValuesResourceTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        now = datetime.now()

        self.series = Series(name="Test series")
        self.area = Area(name="livingroom")
        self.device = Device(82, 1, '0xAAAA', area=self.area)
        self.device_series = DeviceSeries(self.device, self.series)
        self.value = DataPoint(self.device_series, 10, created_at=now)

        self.insert(self.device)
        self.insert(self.series)
        self.insert(self.value)

    def test_dashboard(self):

        r = self.client.get('/')

        self.assertEqual(200, r.status_code)

    def test_area(self):

        r = self.client.get('/areas/livingroom/')

        self.assertEqual(200, r.status_code)

    def test_device(self):

        r = self.client.get('/device/1/')

        self.assertEqual(404, r.status_code)
