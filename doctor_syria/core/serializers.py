from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from pharmacy.choices import MedicineCategory, MedicineForm, StorageCondition
from pharmacy.models import (
    ExpiryAlert,
    Inventory,
    Medicine,
    Order,
    OrderItem,
    StockAlert,
)

User = get_user_model()


class BaseModelSerializer(serializers.ModelSerializer):
    """
    قالب أساسي لجميع المسلسلات في النظام
    يحتوي على الحقول المشتركة والوظائف المساعدة
    """

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    updated_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    def get_field_names(self, declared_fields, info):
        """
        إضافة دعم لتحديد الحقول المطلوبة عبر معامل fields في URL
        مثال: ?fields=id,name,price
        """
        fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, "dynamic_fields", False):
            params = self.context["request"].query_params.get("fields")
            if params:
                fields = params.split(",")

        return fields

    def validate_empty_values(self, data):
        """
        التحقق من القيم الفارغة وتحويلها إلى None
        """
        if isinstance(data, dict):
            return {
                key: (None if value == "" else value) for key, value in data.items()
            }
        return data

    @property
    def current_user(self):
        """
        الحصول على المستخدم الحالي من السياق
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None

    def create(self, validated_data):
        """
        إضافة المستخدم الحالي تلقائياً عند الإنشاء
        """
        if not validated_data.get("created_by") and self.current_user:
            validated_data["created_by"] = self.current_user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        إضافة المستخدم الحالي تلقائياً عند التحديث
        """
        if not validated_data.get("updated_by") and self.current_user:
            validated_data["updated_by"] = self.current_user
        return super().update(instance, validated_data)

    class Meta:
        abstract = True
        fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]
        dynamic_fields = True


class SoftDeleteModelSerializer(BaseModelSerializer):
    """
    قالب للنماذج التي تدعم الحذف الناعم
    """

    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)
    deleted_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        abstract = True
        fields = BaseModelSerializer.Meta.fields + [
            "is_deleted",
            "deleted_at",
            "deleted_by",
        ]


class MedicineListSerializer(serializers.ModelSerializer):
    """
    مسلسل مختصر للأدوية للاستخدام في القوائم المنسدلة
    """

    class Meta:
        model = Medicine
        fields = ["id", "name", "scientific_name", "price", "is_available"]


class MedicineSerializer(SoftDeleteModelSerializer):
    """
    مسلسل الأدوية
    """

    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )
    form_display = serializers.CharField(source="get_form_display", read_only=True)
    storage_condition_display = serializers.CharField(
        source="get_storage_condition_display", read_only=True
    )
    is_expired = serializers.BooleanField(read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)
    inventory_quantity = serializers.IntegerField(
        source="inventory.quantity", read_only=True
    )

    class Meta:
        model = Medicine
        fields = SoftDeleteModelSerializer.Meta.fields + [
            "name",
            "scientific_name",
            "category",
            "category_display",
            "form",
            "form_display",
            "manufacturer",
            "description",
            "dosage",
            "storage_condition",
            "storage_condition_display",
            "price",
            "requires_prescription",
            "is_available",
            "image",
            "barcode",
            "expiry_date",
            "side_effects",
            "contraindications",
            "interactions",
            "notes",
            "is_expired",
            "days_until_expiry",
            "inventory_quantity",
        ]


class OrderItemSerializer(BaseModelSerializer):
    """
    مسلسل عناصر الطلب
    """

    medicine_detail = MedicineListSerializer(source="medicine", read_only=True)

    class Meta:
        model = OrderItem
        fields = BaseModelSerializer.Meta.fields + [
            "order",
            "medicine",
            "medicine_detail",
            "quantity",
            "unit_price",
            "total_price",
            "notes",
        ]

    def validate(self, data):
        """التحقق من توفر الكمية المطلوبة في المخزون"""
        medicine = data["medicine"]
        quantity = data["quantity"]

        try:
            inventory = Inventory.objects.get(medicine=medicine)
            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"الكمية المطلوبة ({quantity}) غير متوفرة في المخزون. المتوفر حالياً: {inventory.quantity}"
                )
        except Inventory.DoesNotExist:
            raise serializers.ValidationError("هذا الدواء غير متوفر في المخزون")

        if medicine.is_expired:
            raise serializers.ValidationError("هذا الدواء منتهي الصلاحية")

        if medicine.requires_prescription and not data.get("prescription"):
            raise serializers.ValidationError("هذا الدواء يتطلب وصفة طبية")

        return data

    def validate_medicine(self, value):
        """التحقق من أن الدواء متاح للبيع"""
        if not value.is_available:
            raise serializers.ValidationError("هذا الدواء غير متاح للبيع حالياً")
        return value


class OrderSerializer(BaseModelSerializer):
    """
    مسلسل الطلبات
    """

    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    items_count = serializers.IntegerField(source="items.count", read_only=True)

    class Meta:
        model = Order
        fields = BaseModelSerializer.Meta.fields + [
            "status",
            "status_display",
            "items",
            "items_count",
            "total_amount",
            "notes",
        ]

    def validate(self, data):
        """التحقق من صحة الطلب"""
        if not self.instance and not self.initial_data.get("items"):
            raise serializers.ValidationError("يجب إضافة عناصر للطلب")
        return data


class InventorySerializer(BaseModelSerializer):
    """
    مسلسل المخزون
    """

    medicine_detail = MedicineListSerializer(source="medicine", read_only=True)
    needs_restock = serializers.BooleanField(read_only=True)
    has_excess = serializers.BooleanField(read_only=True)

    class Meta:
        model = Inventory
        fields = BaseModelSerializer.Meta.fields + [
            "medicine",
            "medicine_detail",
            "quantity",
            "minimum_quantity",
            "maximum_quantity",
            "needs_restock",
            "has_excess",
            "notes",
        ]

    def validate(self, data):
        """التحقق من صحة الكميات"""
        if data.get("minimum_quantity") and data.get("maximum_quantity"):
            if data["minimum_quantity"] >= data["maximum_quantity"]:
                raise serializers.ValidationError(
                    "يجب أن تكون الكمية الدنيا أقل من الكمية القصوى"
                )
        return data


class StockAlertSerializer(BaseModelSerializer):
    """
    مسلسل تنبيهات المخزون
    """

    medicine_detail = MedicineListSerializer(source="medicine", read_only=True)

    class Meta:
        model = StockAlert
        fields = BaseModelSerializer.Meta.fields + [
            "medicine",
            "medicine_detail",
            "alert_type",
            "quantity",
            "threshold",
            "is_resolved",
            "notes",
        ]


class ExpiryAlertSerializer(BaseModelSerializer):
    """
    مسلسل تنبيهات انتهاء الصلاحية
    """

    medicine_detail = MedicineListSerializer(source="medicine", read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)

    class Meta:
        model = ExpiryAlert
        fields = BaseModelSerializer.Meta.fields + [
            "medicine",
            "medicine_detail",
            "expiry_date",
            "days_until_expiry",
            "is_resolved",
            "notes",
        ]
