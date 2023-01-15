from rest_framework.serializers import ModelSerializer
from .models import User


class BowlerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)
