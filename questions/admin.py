from django.contrib import admin
from django.utils.html import format_html
from .models import Question


# --------------------------------------------------
# Custom Admin Actions
# --------------------------------------------------
@admin.action(description="Mark selected questions as Published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="published")


@admin.action(description="Mark selected questions as Draft")
def make_draft(modeladmin, request, queryset):
    queryset.update(status="draft")


# --------------------------------------------------
# Question Admin
# --------------------------------------------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "short_question",
        "subject_name",
        "main_topic_name",
        "sub_topic",
        "difficulty",
        "status_badge",
        "created_by",
        "created_at",
    )

    list_filter = (
        "status",
        "difficulty",
        "sub_topic__main_topic__subject",
        "sub_topic__main_topic",
        "sub_topic",
        "created_at",
    )

    search_fields = (
        "question_text",
        "sub_topic__sub_topic_name",
        "sub_topic__main_topic__topic_name",
        "sub_topic__main_topic__subject__subject_name",
        "created_by__email",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_by", "created_at", "updated_at")

    actions = [make_published, make_draft]

    fieldsets = (
        ("Question Information", {
            "fields": (
                "question_text",
                "sub_topic",
                "difficulty",
                "status",
            )
        }),
        ("Options", {
            "fields": (
                "option_a",
                "option_b",
                "option_c",
                "option_d",
                "correct_answer",
            )
        }),
        ("Additional Help", {
            "fields": (
                "hint",
                "explanation",
            ),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": (
                "created_by",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    # --------------------------------------------------
    # Query Optimization
    # --------------------------------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "sub_topic__main_topic__subject",
            "created_by"
        )

    # --------------------------------------------------
    # Auto-assign created_by
    # --------------------------------------------------
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # --------------------------------------------------
    # Custom Display Helpers
    # --------------------------------------------------
    def short_question(self, obj):
        return obj.question_text[:60] + "..." if len(obj.question_text) > 60 else obj.question_text
    short_question.short_description = "Question"

    def subject_name(self, obj):
        return obj.sub_topic.main_topic.subject.subject_name
    subject_name.admin_order_field = "sub_topic__main_topic__subject__subject_name"
    subject_name.short_description = "Subject"

    def main_topic_name(self, obj):
        return obj.sub_topic.main_topic.topic_name
    main_topic_name.admin_order_field = "sub_topic__main_topic__topic_name"
    main_topic_name.short_description = "Main Topic"

    def status_badge(self, obj):
        if obj.status == "published":
            color = "green"
        else:
            color = "red"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.capitalize(),
        )
    status_badge.short_description = "Status"