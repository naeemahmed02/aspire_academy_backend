from django.db import models
from django.conf import settings
from academics.models import SubTopic
from questions.models import Question


class QuizAttempt(models.Model):

    STATUS_CHOICES = (
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts"
    )

    sub_topic = models.ForeignKey(
        SubTopic, on_delete=models.CASCADE, related_name="quiz_attempts"
    )

    # Configuration Snapshot
    total_questions = models.IntegerField()
    total_marks = models.IntegerField(default=0)
    negative_marking_flag = models.BooleanField(default=False)
    negative_marking = models.FloatField(default=0.0)

    # Timing
    time_limit = models.PositiveBigIntegerField(help_text="Time limit in minutes")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Result
    score = models.FloatField(default=0.0)
    correct_answers = models.PositiveBigIntegerField(default=0)
    wrong_answers = models.PositiveBigIntegerField(default=0)
    skipped_questions = models.PositiveBigIntegerField(default=0)
    accuracy = models.FloatField(default=0.0)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="IN_PROGRESS"
    )

    class Meta:
        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["sub_topic"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.student.email} - {self.sub_topic.sub_topic_name}"


class StudentAnswer(models.Model):

    quiz_attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, related_name="answers"
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_option = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.FloatField(default=0)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("quiz_attempt", "question")
        indexes = [
            models.Index(fields=["quiz_attempt"]),
            models.Index(fields=["question"]),
        ]
