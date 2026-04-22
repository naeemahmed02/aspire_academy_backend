# quizzes/services/analytics_service.py

from quizzes.models import QuizAttempt


class AnalyticsService:

    @staticmethod
    def get_attempt_summary(student, sub_topic):
        """
        Used for dashboards
        """

        attempts = QuizAttempt.objects.filter(
            student=student,
            sub_topic=sub_topic
        )

        return {
            "total_attempts": attempts.count(),
            "avg_score": attempts.aggregate_avg("score"),
        }