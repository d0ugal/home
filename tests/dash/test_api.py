from tests.base import BaseTestCase


from home import app


class DevicesResourceTestCase(BaseTestCase):

    def test_get(self):

        r = self.client.get('/api/devices/')

        self.assertEqual(r, app.url_map)
