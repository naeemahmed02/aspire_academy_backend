from django.db import models
from django.conf import settings
from academics.models import SubTopic
from quizzes.models import QuizAttempt

class StudentProgressSummary(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)

    total_attempts = models.PositiveIntegerField(default=0)

    total_correct_answers = models.PositiveIntegerField(default=0)
    total_wrong_answers = models.PositiveIntegerField(default=0)
    total_skipped_questions = models.PositiveIntegerField(default=0)

    total_score = models.FloatField(default=0)
    average_score = models.FloatField(default=0)
    accuracy = models.FloatField(default=0)

    last_attempt_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "sub_topic")  