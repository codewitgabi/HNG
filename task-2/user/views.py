# third-party imports

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# custom imports

from authentication.serializers import UserSerializer

User = get_user_model()


class GetUserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        auth_user = request.user
        userOrgs = auth_user.organisations.all()
        
        try:
            user = User.objects.get(userId=id)
        except User.DoesNotExist:
            return Response(
                {
                    "status": "Bad request",
                    "message": "Permission denied",
                    "statusCode": 401,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        is_member = any([org.user_set.contains(user) for org in userOrgs])

        if is_member:
            serializer = UserSerializer(user)

            return Response(
                {
                    "status": "success",
                    "message": "<message>",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": "Bad request",
                "message": "Permission denied",
                "statusCode": 401,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
