from unittest import TestCase

from app import create_app
from database import db
from tests.seed import seed_db


class MainTestClass(TestCase):
    def setUp(self):
        self.app = create_app("config.test")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            seed_db()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
