from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

import random

from .models import Question
from .serializers import (
    QuestionWriteSerializer,
    QuestionReadSerializer,
    QuestionListSerializer
)
from .permissions import IsAdminOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Production-grade Question Bank API

    Responsibilities:
    - CRUD Questions
    - Filtering / Search / Ordering
    - Practice mode (random MCQs)
    """

    queryset = Question.objects.select_related(
        "sub_topic",
        "created_by"
    ).all()

    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ["sub_topic", "difficulty", "status"]

    search_fields = ["question_text"]

    ordering_fields = ["created_at", "difficulty"]

    ordering = ["-created_at"]

    # SERIALIZER SWITCHING
    def get_serializer_class(self):

        if self.action == "list":
            return QuestionListSerializer

        if self.action == "retrieve":
            return QuestionReadSerializer

        return QuestionWriteSerializer

    # CREATE QUESTION (ADMIN ONLY)
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # PRACTICE MODE (NO TRACKING)
    @action(detail=False, methods=["get"], url_path="practice")
    def practice(self, request):
        """
        Lightweight MCQ practice mode (NO quiz tracking).
        Used for:
        - Quick revision
        - Topic practice
        """

        sub_topic_id = request.query_params.get("sub_topic")
        difficulty = request.query_params.get("difficulty")

        queryset = self.get_queryset().filter(status="published")

        if sub_topic_id:
            queryset = queryset.filter(sub_topic_id=sub_topic_id)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        # SAFE RANDOMIZATION (PRODUCTION)
        ids = list(queryset.values_list("id", flat=True))
        sample_size = min(len(ids), 20)

        random_ids = random.sample(ids, sample_size) if ids else []

        questions = queryset.filter(id__in=random_ids)

        serializer = QuestionReadSerializer(questions, many=True)

        return Response({
            "count": len(random_ids),
            "results": serializer.data
        })