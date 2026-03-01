from django.contrib import admin
from django.db.models import F
from .models import StudentProgressSummary, StudentProgressHistory


# --------------------------------------------------
# StudentProgressSummary Admin
# --------------------------------------------------
@admin.register(StudentProgressSummary)
class StudentProgressSummaryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "subject_name",
        "main_topic_name",
        "sub_topic",
        "total_attempts",
        "average_score",
        "accuracy",
        "last_attempt_at",
    )

    list_filter = (
        "sub_topic__main_topic__subject",
        "sub_topic__main_topic",
        "sub_topic",
        "last_attempt_at",
    )

    search_fields = (
        "student__email",
        "student__username",
        "sub_topic__sub_topic_name",
        "sub_topic__main_topic__topic_name",
        "sub_topic__main_topic__subject__subject_name",
    )

    ordering = ("-last_attempt_at",)
    readonly_fields = (
        "student",
        "sub_topic",
        "total_attempts",
        "total_correct_answers",
        "total_wrong_answers",
        "total_skipped_questions",
        "total_score",
        "average_score",
        "accuracy",
        "last_attempt_at",
    )

    fieldsets = (
        ("Student & Topic", {
            "fields": ("student", "sub_topic")
        }),
        ("Performance Metrics", {
            "fields": (
                "total_attempts",
                "total_correct_answers",
                "total_wrong_answers",
                "total_skipped_questions",
                "total_score",
                "average_score",
                "accuracy",
            )
        }),
        ("Metadata", {
            "fields": ("last_attempt_at",),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "student",
            "sub_topic__main_topic__subject"
        )

    def subject_name(self, obj):
        return obj.sub_topic.main_topic.subject.subject_name
    subject_name.admin_order_field = "sub_topic__main_topic__subject__subject_name"
    subject_name.short_description = "Subject"

    def main_topic_name(self, obj):
        return obj.sub_topic.main_topic.topic_name
    main_topic_name.admin_order_field = "sub_topic__main_topic__topic_name"
    main_topic_name.short_description = "Main Topic"


# --------------------------------------------------
# StudentProgressHistory Admin
# --------------------------------------------------
@admin.register(StudentProgressHistory)
class StudentProgressHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "quiz_attempt",
        "subject_name",
        "sub_topic",
        "score",
        "correct_answers",
        "wrong_answers",
        "skipped_questions",
        "completed_at",
    )

    list_filter = (
        "sub_topic__main_topic__subject",
        "sub_topic__main_topic",
        "sub_topic",
        "completed_at",
    )

    search_fields = (
        "student__email",
        "student__username",
        "quiz_attempt__id",
        "sub_topic__sub_topic_name",
    )

    ordering = ("-completed_at",)
    date_hierarchy = "completed_at"

    readonly_fields = (
        "student",
        "quiz_attempt",
        "sub_topic",
        "score",
        "correct_answers",
        "wrong_answers",
        "skipped_questions",
        "completed_at",
    )

    fieldsets = (
        ("Student & Attempt Info", {
            "fields": ("student", "quiz_attempt", "sub_topic")
        }),
        ("Result", {
            "fields": (
                "score",
                "correct_answers",
                "wrong_answers",
                "skipped_questions",
            )
        }),
        ("Completion", {
            "fields": ("completed_at",)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "student",
            "quiz_attempt",
            "sub_topic__main_topic__subject"
        )

    def subject_name(self, obj):
        return obj.sub_topic.main_topic.subject.subject_name
    subject_name.admin_order_field = "sub_topic__main_topic__subject__subject_name"
    subject_name.short_description = "Subject"