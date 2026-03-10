from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import StudentProgressSummary, StudentProgressHistory
from .serializers import (
    StudentProgressSummaryListSerializer,
    StudentProgressSummaryDetailSerializer,
    StudentProgressHistorySerializer,
    StudentProgressHistoryListSerializer,
)


class StudentProgressSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Production ViewSet for student progress summary.

    Students → only their progress
    Admins → all progress
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        "sub_topic"
    ]

    ordering_fields = [
        "average_score",
        "accuracy",
        "last_attempt_at"
    ]

    queryset = StudentProgressSummary.objects.select_related(
        "student",
        "sub_topic"
    )

    def get_queryset(self):

        user = self.request.user

        if user.is_staff:
            return self.queryset

        return self.queryset.filter(student=user)

    def get_serializer_class(self):

        if self.action == "list":
            return StudentProgressSummaryListSerializer

        return StudentProgressSummaryDetailSerializer


class StudentProgressHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Production ViewSet for progress history.
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        "sub_topic",
        "quiz_attempt"
    ]

    ordering_fields = [
        "score",
        "completed_at"
    ]

    queryset = StudentProgressHistory.objects.select_related(
        "student",
        "sub_topic",
        "quiz_attempt"
    )

    def get_queryset(self):

        user = self.request.user

        if user.is_staff:
            return self.queryset

        return self.queryset.filter(student=user)

    def get_serializer_class(self):

        if self.action == "list":
            return StudentProgressHistoryListSerializer

        return StudentProgressHistorySerializer