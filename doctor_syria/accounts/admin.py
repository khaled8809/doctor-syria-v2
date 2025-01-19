from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "full_name",
        "user_type",
        "phone",
        "is_verified",
        "is_active",
    )
    list_filter = ("user_type", "is_verified", "is_active", "gender", "city")
    search_fields = ("email", "first_name", "last_name", "phone", "id_number")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("معلومات شخصية"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "father_name",
                    "mother_name",
                    "birth_date",
                    "gender",
                    "marital_status",
                    "blood_type",
                    "phone",
                    "profile_picture",
                )
            },
        ),
        (_("معلومات الهوية"), {"fields": ("id_type", "id_number", "id_picture")}),
        (_("معلومات الموقع"), {"fields": ("address", "city", "region")}),
        (
            _("معلومات مهنية"),
            {
                "fields": (
                    "user_type",
                    "specialty",
                    "license_number",
                    "qualification",
                    "experience_years",
                    "license_picture",
                )
            },
        ),
        (
            _("الصلاحيات"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "verification_date",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type"),
            },
        ),
    )

    def full_name(self, obj):
        return obj.get_full_name()

    full_name.short_description = _("الاسم الكامل")
