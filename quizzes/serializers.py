from rest_framework import serializers
from django.utils import timezone

from .models import QuizAttempt, StudentAnswer
from questions.models import Question



# Student Answer Serializers


class StudentAnswerWriteSerializer(serializers.ModelSerializer):
    """
    Serializer used when a student submits an answer.
    """

    class Meta:
        model = StudentAnswer
        fields = [
            "id",
            "quiz_attempt",
            "question",
            "selected_option",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        """
        Ensure the question belongs to the quiz's subtopic.
        Prevent inconsistent answers.
        """

        attempt = attrs.get("quiz_attempt")
        question = attrs.get("question")

        if question.sub_topic != attempt.sub_topic:
            raise serializers.ValidationError(
                "Question does not belong to this quiz."
            )

        return attrs


class StudentAnswerReadSerializer(serializers.ModelSerializer):
    """
    Used when returning answers with results.
    """

    question_text = serializers.CharField(
        source="question.question_text", read_only=True
    )

    class Meta:
        model = StudentAnswer
        fields = [
            "id",
            "question",
            "question_text",
            "selected_option",
            "is_correct",
            "marks_awarded",
            "answered_at",
        ]



# Quiz Attempt Serializers


class QuizAttemptCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used when starting a quiz.
    """

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "sub_topic",
            "total_questions",
            "total_marks",
            "negative_marking_flag",
            "negative_marking",
            "time_limit",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        Automatically attach the logged-in student.
        """
        user = self.context["request"].user

        return QuizAttempt.objects.create(
            student=user,
            **validated_data
        )


class QuizAttemptListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing attempts.
    """

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "sub_topic_name",
            "score",
            "accuracy",
            "status",
            "started_at",
            "completed_at",
        ]


class QuizAttemptDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer including answers and results.
    """

    answers = StudentAnswerReadSerializer(many=True, read_only=True)

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "student",
            "sub_topic",
            "sub_topic_name",
            "total_questions",
            "total_marks",
            "negative_marking_flag",
            "negative_marking",
            "time_limit",
            "started_at",
            "completed_at",
            "score",
            "correct_answers",
            "wrong_answers",
            "skipped_questions",
            "accuracy",
            "status",
            "answers",
        ]