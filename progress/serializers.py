from rest_framework import serializers
from .models import StudentProgressSummary


# =========================================================
# LIST SERIALIZER
# =========================================================

class StudentProgressSummaryListSerializer(serializers.ModelSerializer):

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = StudentProgressSummary
        fields = [
            "id",
            "sub_topic",
            "sub_topic_name",
            "total_attempts",
            "average_score",
            "accuracy",
            "last_attempt_at",
        ]


# =========================================================
# DETAIL SERIALIZER
# =========================================================

class StudentProgressSummaryDetailSerializer(serializers.ModelSerializer):

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    performance_level = serializers.SerializerMethodField()

    class Meta:
        model = StudentProgressSummary
        fields = [
            "id",
            "student",
            "sub_topic",
            "sub_topic_name",

            "total_attempts",
            "total_correct_answers",
            "total_wrong_answers",
            "total_skipped_questions",

            "total_score",
            "average_score",
            "accuracy",
            "last_attempt_at",

            "performance_level",
        ]

    def get_performance_level(self, obj):
        """
        Simple analytics label (useful for UI)
        """

        if obj.accuracy >= 80:
            return "excellent"
        elif obj.accuracy >= 70:
            return "good"
        elif obj.accuracy >= 60:
            return "average"
        else:
            return "weak"