from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account


# --------------------------------------------------
# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_student",
            'is_teacher',
            'student_id',
            "date_joined",
        )

        read_only_fields = ("id", "date_joined")


# --------------------------------------------------
# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Account
        fields = (
            "email",
            "first_name",
            "last_name",
            'username',
            "password",
        )

    def validate_email(self, value):
        if Account.objects.filter(email = value).exists():
            raise serializers.ValidationError("Email is already in use.")
        
        return value
    
    def create(self, validated_data):
        user = Account.objects.create_user( # type: ignore
            email = validated_data["email"],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username']
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        
        email = attrs.get("email")
        password = attrs.get("password")

        user  = authenticate(email = email, password = password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        
        refresh = RefreshToken.for_user(user)

        return {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("Old password is incorrect.")
        
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user