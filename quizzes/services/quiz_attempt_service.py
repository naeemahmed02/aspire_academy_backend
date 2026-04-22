from django.utils import timezone
from quizzes.models import QuizAttempt
from academics.models import SubTopic
from questions.models import Question


class QuizAttemptService:

    @staticmethod
    def create_attempt(student, sub_topic_id, data):
        """
        Create a new quiz attempt
        """
        print(data)
        sub_topic = SubTopic.objects.get(id=sub_topic_id)

        available_questions = Question.objects.filter(
            sub_topic=sub_topic,
            status="published"
        ).count()

        print("Available questions:", available_questions)

        total_questions = min(
            data.get("total_questions"),
            available_questions
        )
        print("Total questions:", total_questions)


        attempt = QuizAttempt.objects.create(
            student=student,
            sub_topic=sub_topic,
            total_questions=total_questions,
            time_limit=data.get("time_limit", 10),
            status="IN_PROGRESS",
        )

        return attempt

    @staticmethod
    def get_attempt(attempt_id, student):
        """
        Ensure ownership security
        """

        return QuizAttempt.objects.select_related(
            "sub_topic", "student"
        ).get(
            id=attempt_id,
            student=student
        )

    @staticmethod
    def complete_attempt(attempt):
        """
        Mark quiz as completed
        """

        attempt.status = "COMPLETED"
        attempt.completed_at = timezone.now()
        attempt.save()

        return attempt