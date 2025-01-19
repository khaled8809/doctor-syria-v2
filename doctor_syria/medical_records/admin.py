from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Allergy, Appointment, MedicalRecord, Prescription, Vaccination


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "record_type", "title", "date", "severity")
    list_filter = ("record_type", "severity", "doctor", "created_at")
    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "title",
        "description",
    )
    date_hierarchy = "date"
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            _("معلومات أساسية"),
            {"fields": ("patient", "doctor", "record_type", "title", "description")},
        ),
        (_("تفاصيل السجل"), {"fields": ("date", "severity", "notes", "attachments")}),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_type", "scheduled_time", "status")
    list_filter = ("status", "appointment_type", "doctor")
    search_fields = ("patient__user__first_name", "patient__user__last_name", "reason")
    date_hierarchy = "scheduled_time"
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            _("معلومات الموعد"),
            {
                "fields": (
                    "patient",
                    "doctor",
                    "appointment_type",
                    "scheduled_time",
                    "duration",
                )
            },
        ),
        (_("تفاصيل الموعد"), {"fields": ("reason", "notes", "status")}),
        (
            _("معلومات الإلغاء"),
            {"fields": ("cancellation_reason",), "classes": ("collapse",)},
        ),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "medical_record",
        "medicine_name",
        "dosage",
        "is_chronic",
        "refills",
    )
    list_filter = ("is_chronic", "created_at")
    search_fields = ("medicine_name", "medical_record__patient__user__first_name")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            _("معلومات الوصفة"),
            {
                "fields": (
                    "medical_record",
                    "medicine_name",
                    "dosage",
                    "frequency",
                    "duration",
                )
            },
        ),
        (
            _("تفاصيل إضافية"),
            {"fields": ("instructions", "is_chronic", "refills", "notes")},
        ),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("patient", "allergy_type", "allergen", "reaction", "diagnosis_date")
    list_filter = ("allergy_type", "reaction", "diagnosis_date")
    search_fields = ("patient__user__first_name", "allergen")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            _("معلومات الحساسية"),
            {"fields": ("patient", "allergy_type", "allergen", "reaction")},
        ),
        (_("تفاصيل إضافية"), {"fields": ("diagnosis_date", "notes")}),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "vaccine_type",
        "vaccine_name",
        "dose_number",
        "date_given",
    )
    list_filter = ("vaccine_type", "date_given", "given_by")
    search_fields = ("patient__user__first_name", "vaccine_name")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            _("معلومات التطعيم"),
            {"fields": ("patient", "vaccine_type", "vaccine_name", "dose_number")},
        ),
        (_("تفاصيل التطعيم"), {"fields": ("date_given", "given_by", "next_dose_date")}),
        (_("معلومات إضافية"), {"fields": ("batch_number", "manufacturer", "notes")}),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )
