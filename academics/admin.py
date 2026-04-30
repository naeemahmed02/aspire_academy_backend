from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Subject, MainTopic, SubTopic
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm



# --------------------------------------------------
# Subject Admin
# --------------------------------------------------
@admin.register(Subject)
class SubjectAdmin(ModelAdmin, ImportExportModelAdmin):

    list_display = (
        "subject_name",
        "subject_code",
        "created_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "subject_name",
        "subject_code",
    )

    list_filter = (
        "created_by",
    )

    ordering = ("subject_name",)

    import_form_class = ImportForm
    export_form_class = ExportForm

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Subject Details", {
            "fields": (
                "subject_name",
                "subject_code",
                "subject_description",
                "sub_image",
            )
        }),
        ("Audit Info", {
            "fields": (
                "created_by",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )


    # auto assign created_by safely
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# --------------------------------------------------
# SubTopic Inline (for MainTopic)
# --------------------------------------------------
class SubTopicInline(admin.TabularInline):
    model = SubTopic
    extra = 0

    fields = (
        "sub_topic_name",
        "sub_topic_description",
        "created_by",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    show_change_link = True


# --------------------------------------------------
# MainTopic Admin
# --------------------------------------------------
@admin.register(MainTopic)
class MainTopicAdmin(ModelAdmin, ImportExportModelAdmin):

    list_display = (
        "topic_name",
        "subject",
        "created_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "topic_name",
        "subject__subject_name",
    )

    list_filter = (
        "subject",
        "created_by",
    )

    ordering = (
        "subject",
        "topic_name",
    )

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    import_form_class = ImportForm
    export_form_class = ExportForm

    fieldsets = (
        ("Topic Details", {
            "fields": (
                "subject",
                "topic_name",
                "topic_description",
            )
        }),
        ("Audit Info", {
            "fields": (
                "created_by",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    inlines = [SubTopicInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# --------------------------------------------------
# SubTopic Admin
# --------------------------------------------------
@admin.register(SubTopic)
class SubTopicAdmin(ModelAdmin, ImportExportModelAdmin):

    list_display = (
        "sub_topic_name",
        "main_topic",
        "subject_name",
        "created_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "sub_topic_name",
        "main_topic__topic_name",
        "main_topic__subject__subject_name",
    )

    list_filter = (
        "main_topic__subject",
        "main_topic",
        "created_by",
    )

    ordering = (
        "main_topic__subject__subject_name",
        "main_topic__topic_name",
        "sub_topic_name",
    )
    import_form_class = ImportForm
    export_form_class = ExportForm

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Sub Topic Details", {
            "fields": (
                "main_topic",
                "sub_topic_name",
                "sub_topic_description",
            )
        }),
        ("Audit Info", {
            "fields": (
                "created_by",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    def subject_name(self, obj):
        return obj.main_topic.subject.subject_name

    subject_name.admin_order_field = "main_topic__subject__subject_name"
    subject_name.short_description = "Subject"

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)