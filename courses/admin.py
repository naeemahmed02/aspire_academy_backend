from django.contrib import admin

from courses.models import (
    Course,
    Playlist,
    Video,
    Enrollment,
    VideoProgress
)


admin.site.register(Course)
admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Enrollment)
admin.site.register(VideoProgress)