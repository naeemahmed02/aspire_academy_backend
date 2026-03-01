from django.db import models
from accounts.models import Account

class AcademicBaseClass(models.Model):
    created_by = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(class)s_objects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Subject(AcademicBaseClass):
    subject_name = models.CharField(max_length=100, db_index=True)
    subject_code = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    subject_description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ["subject_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject_name"],
                name="unique_subject_name",
            )
        ]

    def __str__(self):
        return self.subject_name


class MainTopic(AcademicBaseClass):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="main_topics",
    )
    topic_name = models.CharField(max_length=100, db_index=True)
    topic_description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Main Topic"
        verbose_name_plural = "Main Topics"
        ordering = ["topic_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "topic_name"],
                name="unique_topic_per_subject",
            )
        ]

    def __str__(self):
        return f"{self.subject.subject_name} - {self.topic_name}"


class SubTopic(AcademicBaseClass):
    main_topic = models.ForeignKey(
        MainTopic,
        on_delete=models.CASCADE,
        related_name="sub_topics",
    )
    sub_topic_name = models.CharField(max_length=100, db_index=True)
    sub_topic_description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Sub Topic"
        verbose_name_plural = "Sub Topics"
        ordering = ["sub_topic_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["main_topic", "sub_topic_name"],
                name="unique_subtopic_per_main_topic",
            )
        ]

    def __str__(self):
        return f"{self.main_topic.topic_name} - {self.sub_topic_name}"
