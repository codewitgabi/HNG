from rest_framework import serializers
from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["orgId", "name", "description"]


class UserSerializer(serializers.Serializer):
    userId = serializers.UUIDField()
