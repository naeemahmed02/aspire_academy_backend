from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Question
from academics.models import SubTopic



# Question Write Serializer
# Used for CREATE and UPDATE operations


class QuestionWriteSerializer(serializers.ModelSerializer):
    """
    Serializer used for creating and updating questions.
    """

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "sub_topic",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "hint",
            "explanation",
            "difficulty",
            "status",
        ]

        read_only_fields = ["id"]

        validators = [
            UniqueTogetherValidator(
                queryset=Question.objects.all(),
                fields=["sub_topic", "question_text"],
                message="This question already exists in this sub-topic."
            )
        ]

    # --------------------------------------------------------
    # Normalize Text Inputs
    # --------------------------------------------------------

    def validate_question_text(self, value):
        return value.strip()

    def validate_option_a(self, value):
        return value.strip()

    def validate_option_b(self, value):
        return value.strip()

    def validate_option_c(self, value):
        return value.strip()

    def validate_option_d(self, value):
        return value.strip()

    # --------------------------------------------------------
    # Cross-field validation
    # --------------------------------------------------------

    def validate(self, attrs):
        option_map = {
            "A": attrs.get("option_a"),
            "B": attrs.get("option_b"),
            "C": attrs.get("option_c"),
            "D": attrs.get("option_d"),
        }

        correct = attrs.get("correct_answer")

        if correct not in option_map:
            raise serializers.ValidationError(
                {"correct_answer": "Invalid answer choice."}
            )

        if not option_map.get(correct):
            raise serializers.ValidationError(
                {"correct_answer": "Correct option must contain text."}
            )

        return attrs



# Question Read Serializer
# Used for detailed question retrieval


class QuestionReadSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for retrieving a single question.
    """

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    created_by = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "sub_topic",
            "sub_topic_name",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "hint",
            "explanation",
            "difficulty",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]



# Question List Serializer
# Lightweight serializer for list endpoints


class QuestionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer used for list APIs.
    Avoids sending heavy fields unnecessarily.
    """

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "sub_topic_name",
            "difficulty",
            "status",
        ]