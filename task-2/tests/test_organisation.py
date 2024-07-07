import json
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from organisation.models import Organisation


User = get_user_model()


class OrganisationTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # create default test user

        cls.default_user = User.objects.create_user(
            firstName="Default",
            lastName="User",
            email="default@gmail.com",
            password="12345",
            phone="+2349020617734",
        )
        cls.default_user2 = User.objects.create_user(
            firstName="Default2",
            lastName="User",
            email="default2@gmail.com",
            password="12345",
            phone="+2349020617734",
        )

        # create default test organisations

        cls.org1 = Organisation.objects.create(name="first org")

        cls.default_user.organisations.add(cls.org1)
        cls.default_user.save()

    def setUp(self):
        self.client = Client()

    def test_users_cant_see_data_from_other_organisations(self):
        """
        * Ensure users can't see data from organisations they don't have access to.
        """

        response1 = self.client.post(
            "/auth/login", {"email": "default@gmail.com", "password": "12345"}
        )
        token = response1.json()["data"]["accessToken"]
        response1 = self.client.get(
            f"/api/users/{self.default_user2.userId}",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response1.status_code, 401)
        self.assertJSONEqual(
            json.dumps(response1.json()),
            {
                "status": "Bad request",
                "message": "Permission denied",
                "statusCode": 401,
            },
        )
