from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "name",
        )


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_active",
            "is_staff",
            "id",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
