from datetime import datetime

from tests.base import BaseTestCase

from home.ts.models import Area, Device, Series, DataPoint, DeviceSeries


class DevicesResourceTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.area = Area(name="livingroom")
        self.device = Device(82, 1, '0xAAAA', area=self.area)
        self.insert(self.device)

    def test_get(self):

        r = self.client.get('/api/devices/')

        self.assertEqual(r.status_code, 200)

    def test_get_id(self):

        r = self.client.get('/api/devices/1')

        self.assertEqual(r.status_code, 200)

    def test_get_404(self):

        r = self.client.get('/api/devices/1000')

        self.assertEqual(r.status_code, 404)


class SeriesResourceTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.series = Series(name="Test series")
        self.insert(self.series)

    def test_get(self):

        r = self.client.get('/api/series/')

        self.assertEqual(r.status_code, 200)

    def test_get_id(self):

        r = self.client.get('/api/series/1')

        self.assertEqual(r.status_code, 200)

    def test_get_name(self):

        r = self.client.get('/api/series/Test series')

        self.assertEqual(r.status_code, 200)

    def test_get_404(self):

        r = self.client.get('/api/series/1000')

        self.assertEqual(r.status_code, 404)


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

    def test_get(self):

        r = self.client.get('/api/values/')

        self.assertEqual(r.status_code, 200)

    def test_get_id(self):

        r = self.client.get('/api/values/1')

        self.assertEqual(r.status_code, 200)

    def test_get_404(self):

        r = self.client.get('/api/values/1000')

        self.assertEqual(r.status_code, 404)
