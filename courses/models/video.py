from django.db import models
from .playlist import Playlist


class Video(models.Model):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name="videos"
    )

    title = models.CharField(max_length=255)

    youtube_video_id = models.CharField(max_length=100)

    duration_seconds = models.PositiveIntegerField(default=0)

    order = models.PositiveIntegerField(default=0)

    is_preview = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        indexes = [
        models.Index(fields=["playlist"]),
        models.Index(fields=["order"]),
    ]

    def __str__(self):
        return self.title