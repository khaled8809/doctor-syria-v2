"""
Admin configuration for the pharmacy application.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Medicine, Prescription, PrescriptionItem


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    Admin configuration for Medicine model.
    """
    list_display = ['name', 'name_ar', 'price', 'quantity', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_ar', 'description', 'description_ar']
    ordering = ['name']
    fieldsets = (
        (_('معلومات أساسية'), {
            'fields': (
                'name', 'name_ar', 'description', 'description_ar',
                'price', 'quantity', 'minimum_quantity', 'is_active'
            )
        }),
        (_('معلومات النظام'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Prescription model.
    """
    list_display = ['patient', 'is_filled', 'created_at']
    list_filter = ['is_filled']
    search_fields = ['patient__user__first_name', 'patient__user__last_name']
    ordering = ['-created_at']
    fieldsets = (
        (_('معلومات الوصفة'), {
            'fields': ('patient', 'notes', 'is_filled')
        }),
        (_('معلومات النظام'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']


class PrescriptionItemInline(admin.TabularInline):
    """
    Inline admin for PrescriptionItem model.
    """
    model = PrescriptionItem
    extra = 1
    fields = ['medicine', 'quantity', 'dosage', 'instructions']


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for PrescriptionItem model.
    """
    list_display = ['prescription', 'medicine', 'quantity', 'dosage']
    list_filter = ['medicine']
    search_fields = ['prescription__patient__user__first_name', 'medicine__name']
    ordering = ['prescription', 'medicine']
    fieldsets = (
        (_('معلومات العنصر'), {
            'fields': ('prescription', 'medicine', 'quantity', 'dosage', 'instructions')
        }),
        (_('معلومات النظام'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']
