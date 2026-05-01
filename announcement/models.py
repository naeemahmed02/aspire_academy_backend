from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()

    is_active = models.BooleanField(default=True)
    is_urgent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title