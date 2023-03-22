from unittest import TestCase

from app import create_app
from database import db
from database.models import User
from flask_sqlalchemy.session import Session
from tests.seed import seed_db
from werkzeug.security import generate_password_hash


class MainTestClass(TestCase):
    token = ""

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

    def create_instance(self, instance):
        with self.app.app_context():
            with Session(db, expire_on_commit=False) as session:
                session.add(instance)
                session.commit()

    def login_by(self, role):
        password = "test password"
        user = User(role=role, password=generate_password_hash(password), email="new_test_mail@example.com")
        self.create_instance(user)
        response = self.client.post("auth/login", json={"email": user.email, "password": password})
        self.assertEqual(response.status_code, 200, f"login failed\n{response.json}")
        self.token = response.json["access_token"]
