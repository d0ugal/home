from home.ts.models import Area, Device, Series, DeviceSeries
from json import dumps

from tests.base import BaseTestCase, BaseRedisTestCase


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


class GraphResourceTestCase(BaseRedisTestCase):

    def setUp(self):
        super().setUp()

        self.area = Area(name="livingroom")
        self.device = Device(82, 1, '0xAAAA', area=self.area)
        self.series = Series(name="Series")
        self.ds = DeviceSeries(self.device, self.series)

        self.insert(self.ds)

    def test_get(self):

        r = self.client.get('/api/graph/')
        self.assertEqual(r.status_code, 404)

    def test_post(self):

        json_string = dumps({
            'device_id': 1,
            'series_id': 1,
            'start': "2014-05-19 20:55:55",
            'end': "2014-05-20 20:55:55",
        })

        r = self.client.post('/api/graph/', data=json_string)
        self.assertEqual(r.json, {'data': {'results': {'full': []}}})
        self.assertEqual(r.status_code, 200)

    def test_post_empty(self):
        r = self.client.post('/api/graph/')
        self.assertEqual(r.status_code, 400)
