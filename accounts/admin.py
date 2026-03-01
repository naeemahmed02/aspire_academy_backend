from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Account


# --------------------------------------------------
# Custom User Creation Form
# --------------------------------------------------
class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "phone_number")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# --------------------------------------------------
# Custom User Change Form
# --------------------------------------------------
class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = "__all__"


# --------------------------------------------------
# Account Admin
# --------------------------------------------------
@admin.register(Account)
class AccountAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_teacher",
        "is_student",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_teacher",
        "is_student",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
    )

    ordering = ("-date_joined",)

    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        ("Login Credentials", {
            "fields": ("email", "username", "password")
        }),
        ("Personal Information", {
            "fields": ("first_name", "last_name", "phone_number")
        }),
        ("Roles", {
            "fields": ("is_teacher", "is_student")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_admin",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": ("date_joined", "last_login"),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = (
        ("Create New User", {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "first_name",
                "last_name",
                "phone_number",
                "password1",
                "password2",
                "is_teacher",
                "is_student",
                "is_staff",
                "is_active",
            ),
        }),
    )