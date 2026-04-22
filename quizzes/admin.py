from django.contrib import admin
from django.utils.html import format_html
from .models import QuizAttempt, StudentAnswer


# --------------------------------------------------
# StudentAnswer Inline (Inside QuizAttempt)
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
class QuizAttemptAdmin(admin.ModelAdmin):

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
        # "total_marks",
        # "negative_marking_flag",
        # "negative_marking",
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
            "fields": ("student", "sub_topic")
        }),
        ("Configuration Snapshot", {
            "fields": (
                "total_questions",
                # "total_marks",
                # "negative_marking_flag",
                # "negative_marking",
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
        qs = super().get_queryset(request)
        return qs.select_related(
            "student",
            "sub_topic__main_topic__subject"
        )

    # --------------------------------------------------
    # Custom Display Fields
    # --------------------------------------------------
    def subject_name(self, obj):
        return obj.sub_topic.main_topic.subject.subject_name
    subject_name.admin_order_field = "sub_topic__main_topic__subject__subject_name"
    subject_name.short_description = "Subject"

    def status_badge(self, obj):
        color_map = {
            "IN_PROGRESS": "orange",
            "COMPLETED": "green",
            "FAILED": "red",
        }
        color = color_map.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.replace("_", " ").title(),
        )
    status_badge.short_description = "Status"


# --------------------------------------------------
# StudentAnswer Admin (Standalone View)
# --------------------------------------------------
@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "quiz_attempt__student",
            "question",
        )

    def student(self, obj):
        return obj.quiz_attempt.student
    student.short_description = "Student"

    def question_short(self, obj):
        text = obj.question.question_text
        return text[:60] + "..." if len(text) > 60 else text
    question_short.short_description = "Question"