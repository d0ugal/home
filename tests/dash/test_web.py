from datetime import datetime

from tests.base import BaseTestCase

from home.ts.models import Device, Series, DataPoint


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

    def test_dashboard(self):

        r = self.client.get('/')

        self.assertEqual(r.status_code, 200)
