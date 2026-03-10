from django.db import transaction
from django.utils import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import QuizAttempt, StudentAnswer
from questions.models import Question

from .serializers import (
    QuizAttemptCreateSerializer,
    QuizAttemptDetailSerializer,
    QuizAttemptListSerializer,
    StudentAnswerWriteSerializer,
)

class QuizAttemptViewSet(viewsets.ModelViewSet):
    """
    Production Grade Quiz Engine

    Supports:
    - Start quiz
    - Fetch quiz questions
    - Submit answers
    - Finish quiz
    - View results
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = QuizAttempt.objects.select_related(
        "student",
        "sub_topic"
    ).prefetch_related("answers")

    
    # Serializer Switching
    

    def get_serializer_class(self):

        if self.action == "create":
            return QuizAttemptCreateSerializer

        if self.action == "list":
            return QuizAttemptListSerializer

        return QuizAttemptDetailSerializer

    
    # Start Quiz
    

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    
    # Get Quiz Questions
    

    @action(detail=True, methods=["get"])
    def questions(self, request, pk=None):

        attempt = self.get_object()

        questions = Question.objects.filter(
            sub_topic=attempt.sub_topic,
            status="published"
        ).order_by("?")[: attempt.total_questions]

        data = []

        for q in questions:
            data.append({
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty
            })

        return Response(data)

    
    # Submit Answer
    

    @action(detail=True, methods=["post"])
    def submit_answer(self, request, pk=None):

        attempt = self.get_object()

        serializer = StudentAnswerWriteSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        selected = serializer.validated_data["selected_option"]

        correct = question.correct_answer

        is_correct = selected == correct

        marks = 1

        if is_correct:
            awarded = marks
        else:
            if attempt.negative_marking_flag:
                awarded = -attempt.negative_marking
            else:
                awarded = 0

        with transaction.atomic():

            StudentAnswer.objects.update_or_create(
                quiz_attempt=attempt,
                question=question,
                defaults={
                    "selected_option": selected,
                    "is_correct": is_correct,
                    "marks_awarded": awarded
                }
            )

        return Response(
            {
                "is_correct": is_correct,
                "marks_awarded": awarded
            },
            status=status.HTTP_200_OK
        )

    
    # Finish Quiz
    

    @action(detail=True, methods=["post"])
    def finish(self, request, pk=None):

        attempt = self.get_object()

        answers = attempt.answers.all()

        correct = answers.filter(is_correct=True).count()
        wrong = answers.filter(is_correct=False).count()

        skipped = attempt.total_questions - answers.count()

        score = sum(a.marks_awarded for a in answers)

        accuracy = 0

        if answers.count() > 0:
            accuracy = (correct / answers.count()) * 100

        attempt.correct_answers = correct
        attempt.wrong_answers = wrong
        attempt.skipped_questions = skipped
        attempt.score = score
        attempt.accuracy = accuracy
        attempt.status = "COMPLETED"
        attempt.completed_at = timezone.now()

        attempt.save()

        serializer = QuizAttemptDetailSerializer(attempt)

        return Response(serializer.data)