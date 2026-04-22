from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .permissions import IsOwnerOrAdmin
from .models import StudentProgressSummary
from .serializers import (
    StudentProgressSummaryListSerializer,
    StudentProgressSummaryDetailSerializer,
)


class StudentProgressSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Production-ready Student Progress API (Simplified)

    ✔ No history table dependency
    ✔ Fully aggregated stats
    ✔ Student isolation
    ✔ Admin full access
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "sub_topic",
    ]

    ordering_fields = [
        "average_score",
        "accuracy",
        "last_attempt_at",
        "total_score",
        "total_attempts",
    ]

    ordering = ["-last_attempt_at"]

    def get_queryset(self):
        user = self.request.user

        qs = StudentProgressSummary.objects.select_related(
            "student",
            "sub_topic"
        )

        # Role-based filtering
        if user.is_staff:
            return qs

        return qs.filter(student=user)

    def get_serializer_class(self):
        if self.action == "list":
            return StudentProgressSummaryListSerializer

        return StudentProgressSummaryDetailSerializer