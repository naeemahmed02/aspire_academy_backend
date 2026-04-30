from django.contrib import admin
from .models import Question
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from django.utils.html import format_html


# =========================================================
# Actions
# =========================================================
@admin.action(description="Mark selected questions as Published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="published")


@admin.action(description="Mark selected questions as Draft")
def make_draft(modeladmin, request, queryset):
    queryset.update(status="draft")


# =========================================================
# Admin
# =========================================================
@admin.register(Question)
class QuestionAdmin(ModelAdmin, ImportExportModelAdmin):

    # -----------------------------
    # LIST DISPLAY
    # -----------------------------
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
    list_per_page = 25

    readonly_fields = ("created_by", "created_at", "updated_at")

    actions = [make_published, make_draft]
    import_form_class = ImportForm
    export_form_class = ExportForm

    # -----------------------------
    # FIELDSETS
    # -----------------------------
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

    # -----------------------------
    # OPTIMIZATION
    # -----------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "sub_topic__main_topic__subject",
            "created_by"
        )

    # -----------------------------
    # AUTO SET USER
    # -----------------------------
    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # -----------------------------
    # DISPLAY HELPERS
    # -----------------------------
    def short_question(self, obj):
        return (obj.question_text[:70] + "...") if len(obj.question_text) > 70 else obj.question_text

    short_question.short_description = "Question"

    def subject_name(self, obj):
        return obj.sub_topic.main_topic.subject.subject_name

    subject_name.short_description = "Subject"
    subject_name.admin_order_field = "sub_topic__main_topic__subject__subject_name"

    def main_topic_name(self, obj):
        return obj.sub_topic.main_topic.topic_name

    main_topic_name.short_description = "Main Topic"
    main_topic_name.admin_order_field = "sub_topic__main_topic__topic_name"

    # -----------------------------
    # STATUS BADGE (FIXED)
    # -----------------------------
    def status_badge(self, obj):
        color = "#16a34a" if obj.status == "published" else "#dc2626"
        label = "Published" if obj.status == "published" else "Draft"

        return format_html(
            '<span style="padding:4px 10px; border-radius:6px; background:{}; color:white; font-weight:600;">{}</span>',
            color,
            label
        )

    status_badge.short_description = "Status"