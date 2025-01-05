from django.contrib import admin
from .models import MedicalRecord, Prescription, LabTest

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = ('patient__username', 'doctor__username', 'diagnosis')
    date_hierarchy = 'created_at'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'medication', 'dosage')
    list_filter = ('medical_record__created_at',)
    search_fields = ('medical_record__patient__username', 'medication')

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'test_name', 'test_date', 'status')
    list_filter = ('test_date', 'status')
    search_fields = ('medical_record__patient__username', 'test_name')
