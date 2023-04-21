from flask_sqlalchemy.model import Model

from database.models import Roles, User
from tests.utils import MainTestClass
from werkzeug.security import check_password_hash


class TestCRUD(MainTestClass):
    urls = ["users", "trainers", "trainings", "subscriptions", "sports", "sub_users"]

    def assert_equal_instance_to_dict(self, instance: Model, data: dict):
        """method to check db.Model instance and dict for equals"""
        for item in data.items():
            self.assertEqual(getattr(instance, item[0]), item[1])

    def test_unauthorized_401(self):
        for url in self.urls:
            get_response = self.client.get(f"/crud/{url}")
            self.assertEqual(get_response.status_code, 401, f"get {url}")

            post_response = self.client.post(f"/crud/{url}")
            self.assertEqual(post_response.status_code, 401, f"post {url}")

            retrieve_response = self.client.get(f"/crud/{url}/1")
            self.assertEqual(retrieve_response.status_code, 401, f"retrieve {url}")

            put_response = self.client.put(f"/crud/{url}/1")
            self.assertEqual(put_response.status_code, 401, f"put {url}")

            delete_response = self.client.delete(f"/crud/{url}/1")
            self.assertEqual(delete_response.status_code, 401, f"delete {url}")

    def test_authorized_not_by_admin_403(self):
        self.login_by(Roles.student)
        for url in self.urls:
            get_response = self.client.get(f"/crud/{url}", headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(get_response.status_code, 403, f"get {url}")

            post_response = self.client.post(f"/crud/{url}", headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(post_response.status_code, 403, f"post {url}")

            retrieve_response = self.client.get(f"/crud/{url}/1", headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(retrieve_response.status_code, 403, f"retrieve {url}")

            put_response = self.client.put(f"/crud/{url}/1", headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(put_response.status_code, 403, f"put {url}")

            delete_response = self.client.delete(f"/crud/{url}/1", headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(delete_response.status_code, 403, f"delete {url}")

    def test_authorized_access_user_ro_endpoint(self):

        self.login_by(Roles.admin)
        url = "users"

        get_response = self.client.get(f"/crud/{url}", headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(get_response.status_code, 200, get_response.json)
        with self.app.app_context():
            self.assertEqual(len(get_response.json), User.query.count())

        post_data = {
            "first_name": "test first name",
            "last_name": "test last name",
            "email": "test@example.com",
            "password": "test pass",
            "role": Roles.student.value,
        }

        post_response = self.client.post(
            f"/crud/{url}", headers={"Authorization": f"Bearer {self.token}"}, json=post_data,
        )
        self.assertEqual(post_response.status_code, 201, post_response.json)
        with self.app.app_context():
            user = User.query.filter_by(id=post_response.json[0]["id"]).first()
        password = post_data.pop("password")
        role = post_data.pop("role")
        self.assertEqual(user.role.value, role)
        self.assertTrue(check_password_hash(user.password, password))
        self.assert_equal_instance_to_dict(user, post_data)

        user_id = post_response.json[0]["id"]

        put_data = {
            "first_name": "test first name",
            "last_name": "test last name",
            "email": "test@example.com",
            "password": "test pass",
            "role": Roles.student.value,
        }
        put_response = self.client.put(
            f"/crud/{url}/{user_id}", headers={"Authorization": f"Bearer {self.token}"}, json=put_data,
        )
        self.assertEqual(put_response.status_code, 200, put_response.json)
        with self.app.app_context():
            user = User.query.filter_by(id=user_id).first()
        password = put_data.pop("password")
        role = put_data.pop("role")
        self.assertEqual(user.role.value, role)
        self.assertTrue(check_password_hash(user.password, password))
        self.assert_equal_instance_to_dict(user, put_data)

        retrieve_response = self.client.get(f"/crud/{url}/{user_id}", headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(retrieve_response.status_code, 200, retrieve_response.json)
        with self.app.app_context():
            user = User.query.filter_by(id=user_id).first()
        retrieve_response_json = {**retrieve_response.json}
        role = retrieve_response_json.pop("role")
        self.assertEqual(user.role.value, role)
        self.assert_equal_instance_to_dict(user, retrieve_response_json)

        with self.app.app_context():
            count_before = User.query.count()
        delete_response = self.client.delete(f"/crud/{url}/{user_id}",
                                             headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(delete_response.status_code, 204)
        with self.app.app_context():
            self.assertEqual(User.query.count(), count_before - 1)
        with self.app.app_context():
            if User.query.filter_by(id=user_id).first():
                self.fail("user has not been deleted")
