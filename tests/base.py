from unittest import TestCase

from home.ts.models import Base
from home.ts import engine


class HomeTestCase(TestCase):

    def setUp(self):

        Base.metadata.create_all(engine)

    def tearDown(self):

        Base.metadata.drop_all(engine)
