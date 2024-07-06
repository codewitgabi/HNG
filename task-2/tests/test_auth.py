import json
from django.test import Client, TestCase
from django.urls import reverse
from organisation.models import Organisation
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class AuthTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.default_user = User.objects.create_user(
            firstName="Default",
            lastName="User",
            email="default@gmail.com",
            password="12345",
            phone="+2349020617734",
        )

    def setUp(self):
        self.client = Client()

    def test_successful_registration(self):
        response = self.client.post(
            "/auth/register",
            {
                "firstName": "Test",
                "lastName": "User",
                "email": "test@gmail.com",
                "password": "12345",
                "phone": "+2349020617734",
            },
        )

        user = User.objects.get(email="test@gmail.com")
        organisation = user.organisations.first()

        expected_response = {
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": response.json()["data"]["accessToken"],
                "user": {
                    "userId": str(user.userId),
                    "firstName": "Test",
                    "lastName": "User",
                    "email": "test@gmail.com",
                    "phone": "+2349020617734",
                },
            },
        }

        """
        * user registration test
        It Should Register User Successfully with Default Organisation:Ensure a user is registered successfully when no organisation details are provided.
        """

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

        """
         * organisation test

        Verify the default organisation name is correctly generated (e.g., "John's Organisation" for a user with the first name "John").
        """

        self.assertIsNotNone(organisation)
        self.assertEqual(organisation.name, "Test's Organisation")

    def test_missing_firstName(self):
        response = self.client.post(
            "/auth/register",
            {
                "lastName": "User",
                "email": "test@gmail.com",
                "password": "12345",
                "phone": "+2349020617734",
            },
        )

        expected_response = {
            "errors": [{"field": "firstName", "message": "This field is required."}]
        }

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

    def test_missing_lastName(self):
        response = self.client.post(
            "/auth/register",
            {
                "firstName": "User",
                "email": "test@gmail.com",
                "password": "12345",
                "phone": "+2349020617734",
            },
        )

        expected_response = {
            "errors": [{"field": "lastName", "message": "This field is required."}]
        }

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

    def test_missing_email(self):
        response = self.client.post(
            "/auth/register",
            {
                "firstName": "Test",
                "lastName": "User",
                "password": "12345",
                "phone": "+2349020617734",
            },
        )

        expected_response = {
            "errors": [{"field": "email", "message": "This field is required."}]
        }

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

    def test_missing_password(self):
        response = self.client.post(
            "/auth/register",
            {
                "firstName": "Test",
                "lastName": "User",
                "email": "test@gmail.com",
                "phone": "+2349020617734",
            },
        )

        expected_response = {
            "errors": [{"field": "password", "message": "This field is required."}]
        }

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

    def test_duplicate_email(self):
        response = self.client.post(
            "/auth/register",
            {
                "firstName": "Test",
                "lastName": "User",
                "email": "default@gmail.com",
                "password": "12345",
                "phone": "+2349020617734",
            },
        )

        expected_response = {
            "errors": [{"field": "email", "message": "User with email already exists"}]
        }

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            "/auth/login", {"email": "default@gmail.com", "password": "12345"}
        )

        expected_response = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": response.json()["data"]["accessToken"],
                "user": {
                    "userId": str(self.default_user.userId),
                    "firstName": self.default_user.firstName,
                    "lastName": self.default_user.lastName,
                    "email": self.default_user.email,
                    "phone": self.default_user.phone.as_e164,
                },
            },
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            "/auth/login", {"email": "default@gmail.com", "password": "0000"}
        )

        expected_response = {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401,
        }

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(json.dumps(response.json()), expected_response)
