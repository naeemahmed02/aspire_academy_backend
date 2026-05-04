from django.db import models
from .course import Course


class Playlist(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="playlists"
    )

    title = models.CharField(max_length=255)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

        indexes = [
        models.Index(fields=["playlist"]),
        models.Index(fields=["order"]),
    ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"