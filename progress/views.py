from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Avg, Count, F
from django.db.models.functions import TruncDay

from .permissions import IsOwnerOrAdmin
from .models import StudentProgressSummary
from .serializers import (
    StudentProgressSummaryListSerializer,
    StudentProgressSummaryDetailSerializer,
)

from quizzes.models import QuizAttempt


# =========================================================
# STUDENT PROGRESS VIEWSET
# =========================================================

class StudentProgressSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Student progress summaries
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin
    ]

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
            "sub_topic",
            "sub_topic__main_topic",
            "sub_topic__main_topic__subject",
        )

        if user.is_staff:
            return qs

        return qs.filter(student=user)

    def get_serializer_class(self):
        if self.action == "list":
            return StudentProgressSummaryListSerializer

        return StudentProgressSummaryDetailSerializer


# =========================================================
# STUDENT DASHBOARD API
# =========================================================

class StudentDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        completed = (
            QuizAttempt.objects
            .filter(
                student=user,
                status="COMPLETED"
            )
            .select_related(
                "sub_topic",
                "sub_topic__main_topic",
                "sub_topic__main_topic__subject",
            )
            .prefetch_related("answers")
        )

        in_progress = (
            QuizAttempt.objects
            .filter(
                student=user,
                status="IN_PROGRESS"
            )
            .select_related(
                "sub_topic"
            )
            .prefetch_related("answers")
        )

        # ----------------------------------
        # OVERALL PERFORMANCE
        # ----------------------------------

        overall = completed.aggregate(
            total_tests=Count("id"),
            avg_score=Avg("score"),
            avg_accuracy=Avg("accuracy"),
        )

        # ----------------------------------
        # SUBJECT PERFORMANCE
        # ----------------------------------

        subject_perf = (
            completed
            .annotate(
                subject_name=F(
                    "sub_topic__main_topic__subject__subject_name"
                )
            )
            .values("subject_name")
            .annotate(
                avg_score=Avg("score"),
                accuracy=Avg("accuracy"),
            )
            .order_by("subject_name")
        )

        # ----------------------------------
        # ASSIGNED / ACTIVE TESTS
        # ----------------------------------

        assigned_tests = []

        for attempt in in_progress[:5]:
            answered_count = attempt.answers.count()

            assigned_tests.append({
                "attempt_id": attempt.id,
                "sub_topic": attempt.sub_topic.sub_topic_name,
                "status": attempt.status,
                "questions_remaining":
                    attempt.total_questions - answered_count,
            })

        # ----------------------------------
        # RECENT RESULTS
        # ----------------------------------

        recent_results = []

        for attempt in completed.order_by("-completed_at")[:5]:
            recent_results.append({
                "sub_topic": attempt.sub_topic.sub_topic_name,
                "score": attempt.score,
                "accuracy": attempt.accuracy,
                "completed_at": attempt.completed_at,
            })

        # ----------------------------------
        # WEEKLY TREND
        # ----------------------------------

        trend = (
            completed
            .annotate(
                day=TruncDay("completed_at")
            )
            .values("day")
            .annotate(
                score=Avg("score")
            )
            .order_by("day")[:7]
        )

        weekly_trend = [
            {
                "day": row["day"].strftime("%a"),
                "score": round(row["score"], 2)
            }
            for row in trend
        ]

        # ----------------------------------
        # RESPONSE
        # ----------------------------------

        return Response({

            "student": {
                "name": getattr(
                    user,
                    "full_name",
                    user.username
                )
            },

            "overall": {
                "total_tests":
                    overall["total_tests"] or 0,

                "avg_score":
                    round(
                        overall["avg_score"] or 0,
                        2
                    ),

                "accuracy":
                    round(
                        overall["avg_accuracy"] or 0,
                        2
                    ),
            },

            "subject_performance":
                list(subject_perf),

            "assigned_tests":
                assigned_tests,

            "recent_results":
                recent_results,

            "weekly_trend":
                weekly_trend,
        })