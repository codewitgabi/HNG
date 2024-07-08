# third-party imports

from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.contrib.auth import get_user_model

# custom imports

from .serializers import LoginSerializer, UserSerializer


User = get_user_model()


class UserRegistrationView(APIView):
    """
    Register user
    """

    @transaction.atomic()
    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        # create access token

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone,
                    },
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if not User.objects.filter(email=email).exists():
            return Response(
                {
                    "status": "Bad request",
                    "message": "Authentication failed",
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = User.objects.get(email=email)

        if not user.check_password(password):
            return Response(
                {
                    "status": "Bad request",
                    "message": "Authentication failed",
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # create access token

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone,
                    },
                },
            },
            status=status.HTTP_200_OK,
        )
