from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsAdminOrReadOnly

from .models import Question
from .serializers import (
    QuestionWriteSerializer,
    QuestionReadSerializer,
    QuestionListSerializer
)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Production-grade ViewSet for Question management.

    Supports:
    - CRUD operations
    - Filtering
    - Search
    - Ordering
    - Optimized queries
    """

    queryset = (
        Question.objects
        .select_related("sub_topic", "created_by")
        .all()
    )

    permission_classes = [IsAdminOrReadOnly]

    # Filtering / Search / Ordering
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "sub_topic",
        "difficulty",
        "status",
    ]

    search_fields = [
        "question_text",
    ]

    ordering_fields = [
        "created_at",
        "difficulty",
    ]

    ordering = ["-created_at"]

    # ---------------------------------------------------------
    # Dynamic Serializer Selection
    # ---------------------------------------------------------
    def get_serializer_class(self):

        if self.action == "list":
            return QuestionListSerializer

        if self.action == "retrieve":
            return QuestionReadSerializer

        return QuestionWriteSerializer

    # ---------------------------------------------------------
    # Automatically assign creator
    # ---------------------------------------------------------
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)