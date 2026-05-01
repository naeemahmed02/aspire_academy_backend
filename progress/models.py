from django.db import models
from django.conf import settings
from academics.models import SubTopic
from quizzes.models import QuizAttempt
from accounts.models import Account

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



class UserActivityEvent(models.Model):
    EVENT_TYPES = (
        ("QUIZ_ATTEMPT", "Quiz Attempt"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event_type}"