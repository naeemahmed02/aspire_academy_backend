from django.db import models
from django.conf import settings
from academics.models import SubTopic
from quizzes.models import QuizAttempt

class StudentProgressSummary(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress_summaries"
    )
    sub_topic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name="student_progress"
    )

    # Aggregated Stats
    total_attempts = models.PositiveBigIntegerField(default=0)
    total_correct_answers = models.PositiveBigIntegerField(default=0)
    total_wrong_answers = models.PositiveBigIntegerField(default=0)
    total_skipped_questions = models.PositiveBigIntegerField(default=0)
    total_score = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)  # percent

    # Last attempt info
    last_attempt_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "sub_topic")
        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["sub_topic"]),
        ]

    def __str__(self):
        return f"{self.student.email} - {self.sub_topic.sub_topic_name}"
    

class StudentProgressHistory(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    quiz_attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE
    )
    sub_topic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE
    )
    score = models.FloatField(default=0.0)
    correct_answers = models.PositiveBigIntegerField(default=0)
    wrong_answers = models.PositiveBigIntegerField(default=0)
    skipped_questions = models.PositiveBigIntegerField(default=0)
    completed_at = models.DateTimeField()