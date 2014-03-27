
from tests.base import HomeTestCase
from home.ts.models import Series, Device, DataPoint
from home.ts import Session


class ModelTestCase(HomeTestCase):

    def setup(self):
        super().setup()
        self.session = Session

    def test_series(self):

        instance = Series(name="testing series")
        self.session.add(instance)

        self.session.commit()
