from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    FollowUp,
    Insurance,
    InsuranceClaim,
    Inventory,
    InventoryTransaction,
    Invoice,
    InvoiceItem,
    LabTest,
    MedicalRecord,
    MedicalReport,
    MedicalVisit,
    Medication,
    Payment,
    Prescription,
    Progress,
    Radiology,
    Treatment,
    Vaccination,
)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ["patient", "blood_type", "created_at", "updated_at"]
    list_filter = ["blood_type", "created_at"]
    search_fields = [
        "patient__first_name",
        "patient__last_name",
        "allergies",
        "chronic_diseases",
    ]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (
            _("Patient Information"),
            {"fields": ("patient", "blood_type", "height", "weight")},
        ),
        (
            _("Medical Information"),
            {
                "fields": (
                    "allergies",
                    "chronic_diseases",
                    "medications",
                    "family_history",
                )
            },
        ),
        (_("Emergency Contact"), {"fields": ("emergency_contact", "emergency_phone")}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(MedicalVisit)
class MedicalVisitAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "visit_type", "visit_date", "created_at"]
    list_filter = ["visit_type", "visit_date", "doctor"]
    search_fields = [
        "patient__first_name",
        "patient__last_name",
        "doctor__first_name",
        "doctor__last_name",
    ]
    readonly_fields = ["created_at"]
    date_hierarchy = "visit_date"
    fieldsets = (
        (
            _("Visit Information"),
            {"fields": ("patient", "doctor", "visit_type", "visit_date")},
        ),
        (
            _("Medical Details"),
            {"fields": ("symptoms", "diagnosis", "treatment", "notes")},
        ),
        (_("Follow-up"), {"fields": ("follow_up_date",)}),
        (
            _("System Information"),
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [
        "visit",
        "medication_name",
        "dosage",
        "frequency",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = [
        "medication_name",
        "visit__patient__first_name",
        "visit__patient__last_name",
    ]
    readonly_fields = ["created_at"]
    fieldsets = (
        (
            _("Prescription Information"),
            {"fields": ("visit", "medication_name", "dosage", "frequency", "duration")},
        ),
        (_("Additional Information"), {"fields": ("instructions", "is_active")}),
        (
            _("System Information"),
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ["visit", "test_name", "status", "test_date", "created_at"]
    list_filter = ["status", "test_date"]
    search_fields = [
        "test_name",
        "visit__patient__first_name",
        "visit__patient__last_name",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "test_date"
    fieldsets = (
        (
            _("Test Information"),
            {"fields": ("visit", "test_name", "description", "status")},
        ),
        (_("Test Details"), {"fields": ("test_date", "results_date", "results")}),
        (_("Additional Information"), {"fields": ("notes",)}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Radiology)
class RadiologyAdmin(admin.ModelAdmin):
    list_display = [
        "visit",
        "radiology_type",
        "body_part",
        "performed_at",
        "created_at",
    ]
    list_filter = ["radiology_type", "performed_at"]
    search_fields = [
        "body_part",
        "visit__patient__first_name",
        "visit__patient__last_name",
    ]
    readonly_fields = ["created_at"]
    date_hierarchy = "performed_at"
    fieldsets = (
        (
            _("Radiology Information"),
            {"fields": ("visit", "radiology_type", "body_part")},
        ),
        (_("Image and Report"), {"fields": ("image", "report")}),
        (_("Additional Information"), {"fields": ("notes", "performed_at")}),
        (
            _("System Information"),
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "vaccine_name",
        "dose_number",
        "date_given",
        "next_due_date",
    ]
    list_filter = ["vaccine_name", "date_given"]
    search_fields = ["patient__first_name", "patient__last_name", "vaccine_name"]
    readonly_fields = ["created_at"]
    date_hierarchy = "date_given"
    fieldsets = (
        (
            _("Vaccination Information"),
            {
                "fields": (
                    "patient",
                    "vaccine_name",
                    "dose_number",
                    "date_given",
                    "next_due_date",
                )
            },
        ),
        (
            _("Administration Details"),
            {"fields": ("administered_by", "batch_number", "manufacturer")},
        ),
        (_("Additional Information"), {"fields": ("notes",)}),
        (
            _("System Information"),
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "generic_name",
        "manufacturer",
        "dosage_form",
        "price",
        "requires_prescription",
    ]
    list_filter = ["requires_prescription", "manufacturer", "dosage_form"]
    search_fields = ["name", "generic_name", "manufacturer"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "generic_name", "manufacturer")}),
        (_("Details"), {"fields": ("description", "dosage_form", "strength", "price")}),
        (_("Requirements"), {"fields": ("requires_prescription",)}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "medication",
        "batch_number",
        "expiry_date",
        "quantity",
        "is_low_stock",
        "is_expired",
    ]
    list_filter = ["medication__manufacturer", "expiry_date"]
    search_fields = ["medication__name", "batch_number", "location"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "expiry_date"
    fieldsets = (
        (
            _("Medication Information"),
            {"fields": ("medication", "batch_number", "expiry_date")},
        ),
        (_("Stock Information"), {"fields": ("quantity", "reorder_level", "location")}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "inventory",
        "transaction_type",
        "quantity",
        "performed_by",
        "created_at",
    ]
    list_filter = ["transaction_type", "created_at", "performed_by"]
    search_fields = ["inventory__medication__name", "reference", "notes"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
    fieldsets = (
        (
            _("Transaction Information"),
            {"fields": ("inventory", "transaction_type", "quantity")},
        ),
        (_("Details"), {"fields": ("reference", "notes", "performed_by")}),
        (
            _("System Information"),
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "report_type",
        "title",
        "is_confidential",
        "created_at",
    ]
    list_filter = ["report_type", "is_confidential", "created_at"]
    search_fields = ["patient__first_name", "patient__last_name", "title", "content"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    fieldsets = (
        (
            _("Report Information"),
            {"fields": ("patient", "doctor", "report_type", "title")},
        ),
        (_("Report Content"), {"fields": ("content", "diagnosis", "recommendations")}),
        (_("Additional Information"), {"fields": ("is_confidential", "attachments")}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "title",
        "priority",
        "status",
        "scheduled_date",
        "is_overdue",
    ]
    list_filter = ["priority", "status", "scheduled_date"]
    search_fields = [
        "patient__first_name",
        "patient__last_name",
        "title",
        "description",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "scheduled_date"
    fieldsets = (
        (
            _("Follow Up Information"),
            {"fields": ("patient", "doctor", "title", "description")},
        ),
        (
            _("Schedule"),
            {"fields": ("scheduled_date", "actual_date", "priority", "status")},
        ),
        (_("Additional Information"), {"fields": ("notes", "reminder_sent")}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = [
        "follow_up",
        "treatment_type",
        "name",
        "frequency",
        "start_date",
        "is_completed",
        "is_active",
    ]
    list_filter = ["treatment_type", "frequency", "is_completed", "start_date"]
    search_fields = [
        "name",
        "description",
        "follow_up__patient__first_name",
        "follow_up__patient__last_name",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "start_date"
    fieldsets = (
        (
            _("Treatment Information"),
            {"fields": ("follow_up", "treatment_type", "name", "description")},
        ),
        (
            _("Schedule"),
            {"fields": ("frequency", "duration", "start_date", "end_date")},
        ),
        (
            _("Instructions and Status"),
            {"fields": ("instructions", "is_completed", "notes")},
        ),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ["treatment", "date", "recorded_by", "created_at"]
    list_filter = ["date", "recorded_by"]
    search_fields = ["treatment__name", "status", "observations"]
    readonly_fields = ["created_at"]
    date_hierarchy = "date"
    fieldsets = (
        (_("Progress Information"), {"fields": ("treatment", "date", "status")}),
        (_("Details"), {"fields": ("observations", "complications", "next_steps")}),
        (_("Recording"), {"fields": ("recorded_by", "created_at")}),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number",
        "patient",
        "status",
        "issue_date",
        "due_date",
        "total",
        "is_overdue",
    ]
    list_filter = ["status", "payment_method", "issue_date", "due_date"]
    search_fields = [
        "invoice_number",
        "patient__first_name",
        "patient__last_name",
        "notes",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "issue_date"
    fieldsets = (
        (
            _("Invoice Information"),
            {"fields": ("invoice_number", "patient", "status", "payment_method")},
        ),
        (_("Dates"), {"fields": ("issue_date", "due_date")}),
        (_("Amounts"), {"fields": ("subtotal", "tax", "discount", "total")}),
        (_("Additional Information"), {"fields": ("notes",)}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ["invoice", "description", "quantity", "unit_price", "total"]
    list_filter = ["invoice__status"]
    search_fields = ["description", "invoice__invoice_number"]
    fieldsets = (
        (_("Invoice Item Information"), {"fields": ("invoice", "description")}),
        (_("Pricing"), {"fields": ("quantity", "unit_price", "total")}),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "amount", "payment_method", "status", "payment_date"]
    list_filter = ["status", "payment_method", "payment_date"]
    search_fields = ["invoice__invoice_number", "transaction_id", "notes"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "payment_date"
    fieldsets = (
        (_("Payment Information"), {"fields": ("invoice", "amount", "payment_method")}),
        (
            _("Transaction Details"),
            {"fields": ("transaction_id", "status", "payment_date")},
        ),
        (_("Additional Information"), {"fields": ("notes",)}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "provider",
        "policy_number",
        "coverage_type",
        "status",
        "start_date",
        "end_date",
        "is_active",
    ]
    list_filter = ["status", "coverage_type", "start_date", "end_date"]
    search_fields = [
        "patient__first_name",
        "patient__last_name",
        "provider",
        "policy_number",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "start_date"
    fieldsets = (
        (
            _("Insurance Information"),
            {"fields": ("patient", "provider", "policy_number", "coverage_type")},
        ),
        (
            _("Coverage Details"),
            {"fields": ("coverage_percentage", "deductible", "max_coverage")},
        ),
        (_("Dates and Status"), {"fields": ("start_date", "end_date", "status")}),
        (_("Additional Information"), {"fields": ("notes",)}),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = [
        "claim_number",
        "insurance",
        "invoice",
        "status",
        "submission_date",
        "amount_claimed",
        "amount_approved",
    ]
    list_filter = ["status", "submission_date", "processed_date", "payment_date"]
    search_fields = [
        "claim_number",
        "insurance__policy_number",
        "invoice__invoice_number",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "submission_date"
    fieldsets = (
        (_("Claim Information"), {"fields": ("claim_number", "insurance", "invoice")}),
        (
            _("Claim Details"),
            {"fields": ("amount_claimed", "amount_approved", "status")},
        ),
        (_("Dates"), {"fields": ("submission_date", "processed_date", "payment_date")}),
        (
            _("Documents and Notes"),
            {"fields": ("documents", "notes", "rejection_reason")},
        ),
        (
            _("System Information"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
