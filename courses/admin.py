from django.contrib import admin
from django.utils.html import format_html

from unfold.admin import ModelAdmin

from courses.models import (
    Course,
    Playlist,
    Video,
    Enrollment,
    VideoProgress,
)


# =========================
# INLINE VIDEOS
# =========================

class VideoInline(admin.TabularInline):
    model = Video
    extra = 0

    fields = (
        "title",
        "youtube_video_id",
        "order",
        "is_preview",
    )

    ordering = ("order",)


# =========================
# COURSE ADMIN
# =========================

@admin.register(Course)
class CourseAdmin(ModelAdmin):

    list_display = (
        "id",
        "title",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
    )

    compressed_fields = True


# =========================
# PLAYLIST ADMIN
# =========================

@admin.register(Playlist)
class PlaylistAdmin(ModelAdmin):

    list_display = (
        "id",
        "title",
        "course",
        "order",
        "created_at",
    )

    list_filter = (
        "course",
    )

    search_fields = (
        "title",
        "course__title",
    )

    ordering = (
        "course",
        "order",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [VideoInline]

    compressed_fields = True


# =========================
# VIDEO ADMIN
# =========================

@admin.register(Video)
class VideoAdmin(ModelAdmin):

    list_display = (
        "id",
        "title",
        "playlist",
        "order",
        "is_preview",
        "youtube_preview",
    )

    list_filter = (
        "is_preview",
        "playlist",
    )

    search_fields = (
        "title",
        "youtube_video_id",
    )

    ordering = (
        "playlist",
        "order",
    )

    autocomplete_fields = (
        "playlist",
    )

    compressed_fields = True

    @admin.display(description="YouTube")
    def youtube_preview(self, obj):

        url = (
            f"https://www.youtube.com/watch?v="
            f"{obj.youtube_video_id}"
        )

        return format_html(
            '<a href="{}" target="_blank">Open Video</a>',
            url,
        )


# =========================
# ENROLLMENT ADMIN
# =========================

@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):

    list_display = (
        "id",
        "user",
        "course",
        "is_active",
        "enrolled_at",
        "expires_at",
    )

    list_filter = (
        "is_active",
        "course",
    )

    search_fields = (
        "user__email",
        "course__title",
    )

    autocomplete_fields = (
        "user",
        "course",
    )

    ordering = (
        "-enrolled_at",
    )

    readonly_fields = (
        "enrolled_at",
    )

    compressed_fields = True


# =========================
# VIDEO PROGRESS ADMIN
# =========================

@admin.register(VideoProgress)
class VideoProgressAdmin(ModelAdmin):

    list_display = (
        "id",
        "user",
        "video",
        "watched_seconds",
        "completed",
        "updated_at",
    )

    list_filter = (
        "completed",
    )

    search_fields = (
        "user__email",
        "video__title",
    )

    autocomplete_fields = (
        "user",
        "video",
    )

    ordering = (
        "-updated_at",
    )

    readonly_fields = (
        "updated_at",
    )

    compressed_fields = True