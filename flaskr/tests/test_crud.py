from tests.utils import MainTestClass


class TestUnAuthorizedAccess(MainTestClass):
    def test_unauthorized_401(self):
        urls = ["users", "trainers", "trainings", "subscriptions", "sports", "sub_users"]

        for url in urls:
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
