from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import UserSerializer


class GetUserDetail(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(
            {
                "status": "success",
                "message": "<message>",
                "data": serializer.data,
            }
        )
