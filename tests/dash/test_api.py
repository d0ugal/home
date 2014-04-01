from datetime import datetime

from tests.base import BaseTestCase

from home.ts.models import Device, Series, DataPoint


class DevicesResourceTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.device = Device(82, 1, '0xAAAA', name="Test device")
        self.insert(self.device)

    def test_get(self):

        r = self.client.get('/api/devices/')

        self.assertEqual(r.status_code, 200)

    def test_get_id(self):

        r = self.client.get('/api/devices/1')

        self.assertEqual(r.status_code, 200)

    def test_get_name(self):

        r = self.client.get('/api/devices/Test device')

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
        self.device = Device(82, 1, '0xAAAA', name="Test device")
        self.value = DataPoint(self.series, self.device, 10, created_at=now)

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


class SeriesRangeResourceTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        now = datetime.now()

        self.series = Series(name="series_a")
        self.device = Device(82, 1, '0xAAAA', name="device_a")
        self.value = DataPoint(self.series, self.device, 10, created_at=now)

        self.insert(self.device)
        self.insert(self.series)
        self.insert(self.value)

    def test_get(self):

        r = self.client.get(
            '/data/series_a/device_a/2014-03-27 00:00/2014-03-28 00:00/')

        self.assertEqual(r.status_code, 200)
