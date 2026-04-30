from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import QuizAttempt, StudentAnswer


# --------------------------------------------------
# StudentAnswer Inline (inside QuizAttempt)
# --------------------------------------------------
class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer

    extra = 0

    readonly_fields = (
        "question",
        "selected_option",
        "is_correct",
        "marks_awarded",
        "answered_at",
    )

    can_delete = False
    show_change_link = False


# --------------------------------------------------
# QuizAttempt Admin
# --------------------------------------------------
@admin.register(QuizAttempt)
class QuizAttemptAdmin(ModelAdmin):

    list_display = (
        "student",
        "subject_name",
        "sub_topic",
        "status_badge",
        "score",
        "accuracy",
        "total_questions",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "status",
        "sub_topic__main_topic__subject",
        "sub_topic__main_topic",
        "sub_topic",
        "started_at",
        "completed_at",
    )

    search_fields = (
        "student__email",
        "student__username",
        "sub_topic__sub_topic_name",
    )

    ordering = ("-started_at",)
    date_hierarchy = "started_at"

    readonly_fields = (
        "student",
        "sub_topic",
        "total_questions",
        "time_limit",
        "started_at",
        "completed_at",
        "score",
        "correct_answers",
        "wrong_answers",
        "skipped_questions",
        "accuracy",
        "status",
    )

    inlines = [StudentAnswerInline]

    fieldsets = (
        ("Student & Topic Info", {
            "fields": (
                "student",
                "sub_topic",
            )
        }),
        ("Configuration Snapshot", {
            "fields": (
                "total_questions",
                "time_limit",
            )
        }),
        ("Results", {
            "fields": (
                "score",
                "correct_answers",
                "wrong_answers",
                "skipped_questions",
                "accuracy",
                "status",
            )
        }),
        ("Timing", {
            "fields": (
                "started_at",
                "completed_at",
            )
        }),
    )

    # --------------------------------------------------
    # Query Optimization
    # --------------------------------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "student",
            "sub_topic__main_topic__subject",
        )

    # --------------------------------------------------
    # Display Helpers
    # --------------------------------------------------
    def subject_name(self, obj):
        return obj.sub_topic.main_topic.subject.subject_name

    subject_name.admin_order_field = "sub_topic__main_topic__subject__subject_name"
    subject_name.short_description = "Subject"

    def status_badge(self, obj):
        status_colors = {
            "IN_PROGRESS": "#f59e0b",  # orange
            "COMPLETED": "#16a34a",    # green
            "FAILED": "#dc2626",       # red
        }

        color = status_colors.get(obj.status, "#111827")

        return format_html(
            '<span style="padding:4px 10px; border-radius:6px; '
            'background:{}; color:white; font-weight:600;">{}</span>',
            color,
            obj.status.replace("_", " ").title(),
        )

    status_badge.short_description = "Status"


# --------------------------------------------------
# StudentAnswer Admin (Standalone)
# --------------------------------------------------
@admin.register(StudentAnswer)
class StudentAnswerAdmin(ModelAdmin):

    list_display = (
        "quiz_attempt",
        "student",
        "question_short",
        "selected_option",
        "is_correct",
        "marks_awarded",
        "answered_at",
    )

    list_filter = (
        "is_correct",
        "answered_at",
        "quiz_attempt__sub_topic__main_topic__subject",
    )

    search_fields = (
        "quiz_attempt__student__email",
        "quiz_attempt__student__username",
        "question__question_text",
    )

    ordering = ("-answered_at",)
    date_hierarchy = "answered_at"

    readonly_fields = (
        "quiz_attempt",
        "question",
        "selected_option",
        "is_correct",
        "marks_awarded",
        "answered_at",
    )

    # --------------------------------------------------
    # Query Optimization
    # --------------------------------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "quiz_attempt__student",
            "question",
        )

    # --------------------------------------------------
    # Display Helpers
    # --------------------------------------------------
    def student(self, obj):
        return obj.quiz_attempt.student

    student.short_description = "Student"

    def question_short(self, obj):
        text = obj.question.question_text
        return text[:60] + "..." if len(text) > 60 else text

    question_short.short_description = "Question"