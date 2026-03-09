import logging
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)

logger = logging.getLogger(__name__)



# Custom Throttle for Authentication Endpoints

class AuthRateThrottle(UserRateThrottle):
    scope = "auth"



# Register View

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()

        logger.info(f"User registered successfully: {user.id}")

        return Response(
            {
                "success": True,
                "message": "User registered successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )



# Login View

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data.get("user")
        logger.info(f"User login successful: {user_data.get('id')}")

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )



# Profile View

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )



# Change Password View

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthRateThrottle]

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

        logger.info(f"Password changed for user: {request.user.id}")

        return Response(
            {
                "success": True,
                "message": "Password changed successfully.",
            },
            status=status.HTTP_200_OK,
        )



# Logout View (With Token Ownership Validation)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)

            # 🔐 Validate token ownership
            if token["user_id"] != request.user.id:
                logger.warning(
                    f"Token ownership mismatch for user {request.user.id}"
                )
                return Response(
                    {
                        "success": False,
                        "message": "Token does not belong to this user.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token.blacklist()

            logger.info(f"User logged out successfully: {request.user.id}")

            return Response(
                {
                    "success": True,
                    "message": "Logged out successfully.",
                },
                status=status.HTTP_205_RESET_CONTENT,
            )

        except TokenError:
            logger.warning(
                f"Invalid or expired refresh token used by user {request.user.id}"
            )
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )