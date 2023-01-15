from rest_framework.serializers import ModelSerializer
from .models import User


class BowlerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
