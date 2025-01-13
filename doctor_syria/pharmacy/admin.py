from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Medicine, Inventory, Order, OrderItem, StockAlert, ExpiryAlert


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    إدارة الأدوية
    """

    list_display = [
        "name",
        "scientific_name",
        "category",
        "form",
        "price",
        "is_available",
    ]
    list_filter = [
        "category",
        "form",
        "requires_prescription",
        "is_available",
        "created_at",
    ]
    search_fields = ["name", "scientific_name", "manufacturer", "barcode"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
    fieldsets = (
        (
            _("معلومات أساسية"),
            {
                "fields": (
                    "name",
                    "scientific_name",
                    "category",
                    "form",
                    "manufacturer",
                    "description",
                )
            },
        ),
        (
            _("معلومات فنية"),
            {
                "fields": (
                    "dosage",
                    "storage_condition",
                    "price",
                    "requires_prescription",
                    "is_available",
                    "barcode",
                )
            },
        ),
        (
            _("معلومات إضافية"),
            {
                "fields": (
                    "side_effects",
                    "contraindications",
                    "interactions",
                    "notes",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """
    إدارة المخزون
    """

    list_display = ["medicine", "batch_number", "quantity", "expiry_date"]
    list_filter = ["medicine__category", "supplier", "purchase_date", "expiry_date"]
    search_fields = ["medicine__name", "batch_number", "supplier"]
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
    fieldsets = (
        (
            _("معلومات المخزون"),
            {"fields": ("medicine", "batch_number", "quantity", "unit_cost")},
        ),
        (
            _("معلومات التوريد"),
            {"fields": ("supplier", "purchase_date", "expiry_date", "notes")},
        ),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


class OrderItemInline(admin.TabularInline):
    """
    إدارة عناصر الطلب
    """

    model = OrderItem
    extra = 1
    readonly_fields = ["total_price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    إدارة الطلبات
    """

    list_display = ["id", "patient", "status", "payment_status", "total_amount"]
    list_filter = ["status", "payment_method", "payment_status", "created_at"]
    search_fields = ["patient__name", "delivery_address"]
    readonly_fields = [
        "final_amount",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    ]
    inlines = [OrderItemInline]
    fieldsets = (
        (
            _("معلومات الطلب"),
            {"fields": ("patient", "prescription", "status", "delivery_address")},
        ),
        (
            _("معلومات الدفع"),
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                    "total_amount",
                    "discount",
                    "insurance_coverage",
                    "final_amount",
                )
            },
        ),
        (
            _("ملاحظات"),
            {"fields": ("delivery_notes", "notes"), "classes": ("collapse",)},
        ),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    """
    إدارة تنبيهات المخزون
    """

    list_display = ["medicine", "min_quantity", "current_quantity", "is_resolved"]
    list_filter = ["is_resolved", "created_at"]
    search_fields = ["medicine__name"]
    readonly_fields = [
        "resolved_at",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    ]
    fieldsets = (
        (
            _("معلومات التنبيه"),
            {"fields": ("medicine", "min_quantity", "current_quantity", "notes")},
        ),
        (_("حالة التنبيه"), {"fields": ("is_resolved", "resolved_at")}),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ExpiryAlert)
class ExpiryAlertAdmin(admin.ModelAdmin):
    """
    إدارة تنبيهات انتهاء الصلاحية
    """

    list_display = ["medicine", "batch_number", "expiry_date", "is_resolved"]
    list_filter = ["is_resolved", "expiry_date", "created_at"]
    search_fields = ["medicine__name", "batch_number"]
    readonly_fields = [
        "resolved_at",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    ]
    fieldsets = (
        (
            _("معلومات التنبيه"),
            {"fields": ("medicine", "batch_number", "expiry_date", "quantity")},
        ),
        (
            _("حالة التنبيه"),
            {"fields": ("is_resolved", "resolved_at", "resolution_notes")},
        ),
        (
            _("معلومات النظام"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )
