from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from organisation.models import Organisation
from organisation.serializers import OrganisationSerializer, UserSerializer


User = get_user_model()


class ListCreateOrganisations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = request.user.organisations.all()
        serializer = OrganisationSerializer(queryset, many=True)

        return Response(
            {
                "status": "success",
                "message": "<message>",
                "data": {"organisations": serializer.data},
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        organisation = serializer.save()

        user.organisations.add(organisation)
        user.save()

        return Response(
            {
                "status": "success",
                "message": "Organisation created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class GetOrganisation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orgId: str):
        organisation = request.user.organisations.get(orgId=orgId)
        print(organisation)
        serializer = OrganisationSerializer(organisation)

        return Response(
            {
                "status": "success",
                "message": "<message>",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AddUserToOrganisation(APIView):
    def post(self, request, orgId):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userId = serializer.validated_data.get("userId")
        user = User.objects.get(userId=userId)

        organisation = Organisation.objects.get(orgId=orgId)
        user.organisations.add(organisation)

        return Response(
            {
                "status": "success",
                "message": "User added to organisation successfully",
            },
            status=status.HTTP_200_OK,
        )
