from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account

# --------------------------------------------------
# User Registration Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            "id",
            "email",
            "full_name",
            "is_student",
            "date_joined",
        )

        read_only_fields = ("id", "date_joined")
        