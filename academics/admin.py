from django.contrib import admin
from .models import Subject, MainTopic, SubTopic


# -------------------------------
# Subject Admin
# -------------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_name", "subject_code", "created_by", "created_at", "updated_at")
    search_fields = ("subject_name", "subject_code")
    list_filter = ("created_by",)
    ordering = ("subject_name",)
    readonly_fields = ("created_by", "created_at", "updated_at")
    
    fieldsets = (
        (None, {
            "fields": ("subject_name", "subject_code", "subject_description")
        }),
        ("Audit Info", {
            "fields": ("created_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


# -------------------------------
# SubTopic Inline for MainTopic
# -------------------------------
class SubTopicInline(admin.TabularInline):
    model = SubTopic
    extra = 0
    readonly_fields = ("created_by", "created_at", "updated_at")
    fields = ("sub_topic_name", "sub_topic_description", "created_by", "created_at", "updated_at")
    show_change_link = True


# -------------------------------
# MainTopic Admin
# -------------------------------
@admin.register(MainTopic)
class MainTopicAdmin(admin.ModelAdmin):
    list_display = ("topic_name", "subject", "created_by", "created_at", "updated_at")
    search_fields = ("topic_name", "subject__subject_name")
    list_filter = ("subject", "created_by")
    ordering = ("subject", "topic_name")
    readonly_fields = ("created_by", "created_at", "updated_at")
    
    fieldsets = (
        (None, {
            "fields": ("subject", "topic_name", "topic_description")
        }),
        ("Audit Info", {
            "fields": ("created_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    inlines = [SubTopicInline]


# -------------------------------
# SubTopic Admin
# -------------------------------
@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ("sub_topic_name", "main_topic", "subject_name", "created_by", "created_at", "updated_at")
    search_fields = ("sub_topic_name", "main_topic__topic_name", "main_topic__subject__subject_name")
    list_filter = ("main_topic__subject", "main_topic", "created_by")
    ordering = ("main_topic__subject__subject_name", "main_topic__topic_name", "sub_topic_name")
    readonly_fields = ("created_by", "created_at", "updated_at")
    
    fieldsets = (
        (None, {
            "fields": ("main_topic", "sub_topic_name", "sub_topic_description")
        }),
        ("Audit Info", {
            "fields": ("created_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    # Helper method to display Subject in list display
    def subject_name(self, obj):
        return obj.main_topic.subject.subject_name
    subject_name.admin_order_field = "main_topic__subject__subject_name"
    subject_name.short_description = "Subject"