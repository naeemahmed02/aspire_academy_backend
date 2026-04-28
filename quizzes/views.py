import random

from django.db import transaction

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import QuizAttempt
from questions.models import Question

from .serializers import (
    QuizAttemptCreateSerializer,
    QuizAttemptDetailSerializer,
    QuizAttemptListSerializer,
    StudentAnswerWriteSerializer,
)

# SERVICES
from quizzes.services.quiz_attempt_service import QuizAttemptService
from quizzes.services.answer_service import AnswerService
from quizzes.services.scoring_service import ScoringService


# class QuizAttemptViewSet(viewsets.ModelViewSet):
#     """
#     Production Grade Quiz Engine (Service-Based Architecture)

#     Responsibilities:
#     - Orchestrates API flow
#     - Delegates logic to services
#     - Keeps endpoints clean & scalable
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     queryset = QuizAttempt.objects.select_related(
#         "student", "sub_topic"
#     ).prefetch_related("answers")

#     # =========================
#     # SERIALIZER SWITCH
#     # =========================
#     def get_serializer_class(self):

#         if self.action == "create":
#             return QuizAttemptCreateSerializer

#         if self.action == "list":
#             return QuizAttemptListSerializer

#         return QuizAttemptDetailSerializer

#     # =========================
#     # CREATE ATTEMPT
#     # =========================
#     def perform_create(self, serializer):
#         serializer.save(student=self.request.user)

#     # =========================
#     # GET QUESTIONS (LOCKED)
#     # =========================
#     @action(detail=True, methods=["get"])
#     def questions(self, request, pk=None):

#         attempt = self.get_object()

#         if attempt.status == "COMPLETED":
#             return Response({"error": "Quiz already completed"}, status=400)

#         # If already assigned → reuse
#         if attempt.questions.exists():
#             questions = attempt.questions.all()

#         else:
#             qs = Question.objects.filter(
#                 sub_topic=attempt.sub_topic,
#                 status="published"
#             )

#             ids = list(qs.values_list("id", flat=True))

#             if not ids:
#                 return Response({"error": "No questions available"}, status=400)

#             selected_ids = random.sample(
#                 ids,
#                 min(len(ids), attempt.total_questions)
#             )

#             questions = qs.filter(id__in=selected_ids)

#             # SAVE LOCKED QUESTIONS
#             attempt.questions.set(questions)

#         data = [
#             {
#                 "id": q.id,
#                 "question_text": q.question_text,
#                 "options": [
#                     q.option_a,
#                     q.option_b,
#                     q.option_c,
#                     q.option_d,
#                 ],
#                 "difficulty": q.difficulty,
#             }
#             for q in questions
#         ]

#         return Response(data)

#     # =========================
#     # SUBMIT ANSWER
#     # =========================
#     @action(detail=True, methods=["post"])
#     def submit_answer(self, request, pk=None):

#         attempt = QuizAttemptService.get_attempt(pk, request.user)

#         if attempt.status == "COMPLETED":
#             return Response(
#                 {"error": "Quiz already completed"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = StudentAnswerWriteSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         question = serializer.validated_data["question"]
#         selected = serializer.validated_data["selected_option"]

#         answer, error = AnswerService.submit_answer(
#             attempt=attempt,
#             question=question,
#             selected_option=selected,
#         )

#         if error:
#             return Response(
#                 {"error": error},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return Response({
#             "is_correct": answer.is_correct,
#             "marks_awarded": answer.marks_awarded
#         }, status=status.HTTP_200_OK)

#     # =========================
#     # FINISH QUIZ
#     # =========================
#     @action(detail=True, methods=["post"])
#     def finish(self, request, pk=None):

#         attempt = QuizAttemptService.get_attempt(pk, request.user)

#         if attempt.status == "COMPLETED":
#             return Response(
#                 {"error": "Already completed"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with transaction.atomic():

#             # Calculate results
#             result = ScoringService.calculate(attempt)

#             # Apply results
#             ScoringService.apply(attempt, result)

#             # Mark complete
#             QuizAttemptService.complete_attempt(attempt)

#             # FUTURE HOOK
#             # ProgressService.update(attempt)

#         return Response(
#             QuizAttemptDetailSerializer(attempt).data,
#             status=status.HTTP_200_OK
#         )


class QuizAttemptViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    queryset = QuizAttempt.objects.select_related(
        "student", "sub_topic"
    ).prefetch_related("answers")

    # =========================
    # SERIALIZER SWITCH
    # =========================
    def get_serializer_class(self):
        if self.action == "create":
            return QuizAttemptCreateSerializer
        if self.action == "list":
            return QuizAttemptListSerializer
        return QuizAttemptDetailSerializer

    # =========================
    # CREATE ATTEMPT
    # =========================
    # def perform_create(self, serializer):
    #     serializer.save(student=self.request.user)
    # def perform_create(self, serializer):
    #     attempt = QuizAttemptService.create_attempt(
    #         student=self.request.user,
    #         sub_topic_id=serializer.validated_data["sub_topic"].id,
    #         data=serializer.validated_data
    #     )
    #     return attempt

    @action(detail=False, methods=["get"])
    def recent(self, request):
        attempts = QuizAttempt.objects.filter(
            student=request.user,
            status="COMPLETED"
        ).order_by("-completed_at")[:5]

        serializer = QuizAttemptListSerializer(attempts, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt = QuizAttemptService.create_attempt(
            student=request.user,
            sub_topic_id=serializer.validated_data["sub_topic"].id,
            data=serializer.validated_data,
        )

        return Response(
            QuizAttemptCreateSerializer(attempt, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    # =========================
    # GET QUESTIONS
    # =========================
    @action(detail=True, methods=["get"])
    def questions(self, request, pk=None):

        attempt = self.get_object()

        if attempt.status == "COMPLETED":
            return Response(
                {"error": "Quiz already completed"}, status=status.HTTP_400_BAD_REQUEST
            )

        if attempt.questions.exists():
            questions = attempt.questions.all()
        else:
            qs = Question.objects.filter(
                sub_topic=attempt.sub_topic, status="published"
            )

            ids = list(qs.values_list("id", flat=True))

            if not ids:
                return Response(
                    {"error": "No questions available"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            selected_ids = random.sample(ids, min(len(ids), attempt.total_questions))

            questions = qs.filter(id__in=selected_ids)
            attempt.questions.set(questions)

        data = [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": [
                    q.option_a,
                    q.option_b,
                    q.option_c,
                    q.option_d,
                ],
                "difficulty": q.difficulty,
            }
            for q in questions
        ]

        return Response(data, status=status.HTTP_200_OK)

    # SUBMIT ANSWER (FIXED)
    @action(detail=True, methods=["post"])
    def submit_answer(self, request, pk=None):

        try:
            attempt = QuizAttemptService.get_attempt(pk, request.user)

            if attempt.status == "COMPLETED":
                return Response(
                    {"error": "Quiz already completed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = StudentAnswerWriteSerializer(
                data=request.data, context={"request": request, "attempt": attempt}
            )

            serializer.is_valid(raise_exception=True)

            question = serializer.validated_data["question"]
            selected = serializer.validated_data["selected_option"]

            answer, error = AnswerService.submit_answer(
                attempt=attempt,
                question=question,
                selected_option=selected,
                time_taken=serializer.validated_data.get("time_taken", 0),
            )

            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {
                    "is_correct": answer.is_correct,
                    "marks_awarded": answer.marks_awarded,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # =========================
    # FINISH QUIZ
    # =========================
    @action(detail=True, methods=["post"])
    def finish(self, request, pk=None):

        attempt = QuizAttemptService.get_attempt(pk, request.user)

        if attempt.status == "COMPLETED":
            return Response(
                {"error": "Already completed"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            result = ScoringService.calculate(attempt)
            ScoringService.apply(attempt, result)
            QuizAttemptService.complete_attempt(attempt)

        return Response(
            QuizAttemptDetailSerializer(attempt).data, status=status.HTTP_200_OK
        )
