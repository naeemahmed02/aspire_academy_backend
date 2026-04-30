from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Q

from .models import Subject, MainTopic, SubTopic
from .serializers import (
    SubjectWriteSerializer,
    SubjectReadSerializer,
    SubjectListSerializer,
    MainTopicWriteSerializer,
    MainTopicReadSerializer,
    MainTopicListSerializer,
    SubTopicWriteSerializer,
    SubTopicReadSerializer,
    SubTopicListSerializer,
)


# SUBJECT VIEWSET
class SubjectViewSet(viewsets.ModelViewSet):

    queryset = Subject.objects.all().prefetch_related("main_topics__sub_topics")
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["subject_name"]
    ordering_fields = ["subject_name", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectListSerializer
        if self.action == "retrieve":
            return SubjectReadSerializer
        return SubjectWriteSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# MAIN TOPIC VIEWSET
class MainTopicViewSet(viewsets.ModelViewSet):

    queryset = MainTopic.objects.all().select_related("subject").prefetch_related("sub_topics")
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subject"]

    def get_serializer_class(self):

        if self.action == "list":
            return MainTopicListSerializer

        if self.action == "retrieve":
            return MainTopicReadSerializer

        return MainTopicWriteSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# SUB TOPIC VIEWSET
class SubTopicViewSet(viewsets.ModelViewSet):

    queryset = SubTopic.objects.annotate(
        total_questions=Count(
            'questions',
            filter=Q(questions__status='published')
        )
    ).filter(
        total_questions__gt=0
    ).select_related(
        "main_topic",
        "main_topic__subject"
    )
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["main_topic"]

    def get_serializer_class(self):

        if self.action == "list":
            return SubTopicListSerializer

        if self.action == "retrieve":
            return SubTopicReadSerializer

        return SubTopicWriteSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)