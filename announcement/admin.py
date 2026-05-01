from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "is_urgent",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("is_active", "is_urgent", "created_at")
    search_fields = ("title", "message")
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "message")
        }),
        ("Status", {
            "fields": ("is_active", "is_urgent")
        }),
        ("Schedule", {
            "fields": ("start_date", "end_date")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    readonly_fields = ("created_at", "updated_at")