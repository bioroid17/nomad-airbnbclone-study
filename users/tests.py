from rest_framework.test import APITestCase
from tweets.models import Tweet
from .models import User


class TestUsers(APITestCase):

    USERNAME = "test"
    PASSWORD = "123"
    NAME = "testname"
    URL = "/api/v1/users/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_all_users(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["username"],
            self.USERNAME,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )

    def test_post_user(self):

        new_user_username = "newuser"
        new_user_password = "newpassword"
        new_user_name = "newname"

        response = self.client.post(
            self.URL,
            data={
                "username": new_user_username,
            },
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            self.URL,
            data={
                "password": new_user_password,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.URL,
            data={
                "username": new_user_username,
                "password": new_user_password,
                "name": new_user_name,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["username"],
            new_user_username,
        )
        self.assertEqual(
            data["name"],
            new_user_name,
        )
        self.assertIn("username", data)
        self.assertIn("name", data)
        self.assertNotIn("password", data)


class TestUser(APITestCase):

    USERNAME = "test"
    PASSWORD = "123"
    PAYLOAD = "New Tweet"

    def setUp(self):
        user = User.objects.create(username=self.USERNAME)
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user
        Tweet.objects.create(
            user=user,
            payload=self.PAYLOAD,
        )

    def test_user_not_found(self):
        response = self.client.get("/api/v1/users/2")
        self.assertEqual(response.status_code, 404)

    def test_get_user(self):

        response = self.client.get("/api/v1/users/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data["username"],
            self.USERNAME,
        )

    def test_get_user_tweets(self):

        response = self.client.get("/api/v1/users/1/tweets")
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["user"]["username"],
            self.user.username,
        )
        self.assertEqual(
            data[0]["user"]["name"],
            self.user.name,
        )
        self.assertEqual(
            data[0]["payload"],
            self.PAYLOAD,
        )

    def test_change_password(self):
        old_password = self.PASSWORD
        new_password = "000"
        response = self.client.put(
            "/api/v1/users/password",
            data={
                "old_password": old_password,
                "new_password": new_password,
            },
        )
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)
        response = self.client.put(
            "/api/v1/users/password",
            data={
                "old_password": old_password,
            },
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.put(
            "/api/v1/users/password",
            data={
                "new_password": new_password,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            "/api/v1/users/password",
            data={
                "old_password": old_password,
                "new_password": new_password,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(
            "/api/v1/users/login",
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.post("/api/v1/users/logout")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)
        response = self.client.post("/api/v1/users/logout")
        self.assertEqual(response.status_code, 200)

    def test_jwt(self):
        response = self.client.post(
            "/api/v1/users/jwt-login",
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        data = response.json()
        self.assertIn("token", data)

        response = self.client.post(
            "/api/v1/tweets/",
            headers={
                "jwt": data["token"],
            },
            data={
                "payload": "From JWT",
            },
        )
        self.assertEqual(response.status_code, 200)
