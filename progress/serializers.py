from rest_framework import serializers

from .models import StudentProgressSummary, StudentProgressHistory



# Progress History Serializers


class StudentProgressHistorySerializer(serializers.ModelSerializer):
    """
    Detailed serializer showing results for each quiz attempt.
    """

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = StudentProgressHistory
        fields = [
            "id",
            "quiz_attempt",
            "sub_topic",
            "sub_topic_name",
            "score",
            "correct_answers",
            "wrong_answers",
            "skipped_questions",
            "completed_at",
        ]
        read_only_fields = fields


class StudentProgressHistoryListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing history records.
    """

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = StudentProgressHistory
        fields = [
            "id",
            "sub_topic_name",
            "score",
            "completed_at",
        ]



# Progress Summary Serializers


class StudentProgressSummaryListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer used for dashboard progress overview.
    """

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
        read_only_fields = fields


class StudentProgressSummaryDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer including full performance stats.
    """

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    history = serializers.SerializerMethodField()

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
            "history",
        ]
        read_only_fields = fields

    def get_history(self, obj):
        """
        Return latest attempt history for this student & subtopic.
        """
        histories = obj.sub_topic.quiz_attempts.filter(
            student=obj.student,
            status="COMPLETED"
        ).order_by("-completed_at")[:10]

        return [
            {
                "attempt_id": h.id,
                "score": h.score,
                "accuracy": h.accuracy,
                "completed_at": h.completed_at
            }
            for h in histories
        ]