from django.db import models
from django.conf import settings
from .video import Video


class VideoProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="video_progress"
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    watched_seconds = models.PositiveIntegerField(default=0)

    completed = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")
        indexes = [
        models.Index(fields=["playlist"]),
        models.Index(fields=["order"]),
    ]

    def __str__(self):
        return f"{self.user} - {self.video}"