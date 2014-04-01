from os import environ

from flask.ext.testing import TestCase

from home import create_app
from home.ts.models import db

if environ.get('TRAVIS') == 'true':
    _DATABASE_URI = 'postgresql://postgres@localhost:5432/test_home'
else:
    _DATABASE_URI = 'postgresql://home:home@localhost:5432/test_home'


class BaseTestCase(TestCase):

    SQLALCHEMY_DATABASE_URI = _DATABASE_URI
    TESTING = True

    def create_app(self):

        app = create_app(self)

        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], _DATABASE_URI)

        return app

    def setUp(self):

        self.db = db
        self.db.create_all()

    def insert(self, model):
        self.db.session.add(model)
        self.db.session.commit()

    def tearDown(self):

        self.db.session.remove()
        self.db.drop_all()
