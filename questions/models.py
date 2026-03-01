from django.db import models
from django.core.exceptions import ValidationError
from academics.models import SubTopic
from accounts.models import Account


class Question(models.Model):

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    QUESTION_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    # Core Question
    question_text = models.TextField()
    sub_topic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name="questions",
        db_index=True
    )

    # Options
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()

    # Correct Answer
    correct_answer = models.CharField(
        max_length=1,
        choices=(
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        )
    )

    # Extra Info
    hint = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_LEVELS,
        default='medium',
        db_index=True
    )

    status = models.CharField(
        max_length=10,
        choices=QUESTION_STATUS,
        default='draft',
        db_index=True
    )

    created_by = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_questions'
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        constraints = [
            models.UniqueConstraint(
                fields=['sub_topic', 'question_text'],
                name='unique_question_per_subtopic'
            )
        ]

    def clean(self):
        option_map = {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }

        if not option_map.get(self.correct_answer):
            raise ValidationError("Correct answer must have valid option text.")

    def __str__(self):
        return self.question_text[:50]