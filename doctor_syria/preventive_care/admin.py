from django.contrib import admin

from .models import HealthTip, PreventiveCheckup, Vaccination


@admin.register(PreventiveCheckup)
class PreventiveCheckupAdmin(admin.ModelAdmin):
    list_display = ("patient", "checkup_type", "due_date", "completed")
    list_filter = ("completed", "checkup_type")
    search_fields = ("patient__username", "checkup_type")


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ("patient", "vaccine_name", "due_date", "administered_date")
    list_filter = ("vaccine_name",)
    search_fields = ("patient__username", "vaccine_name")


@admin.register(HealthTip)
class HealthTipAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "content")
