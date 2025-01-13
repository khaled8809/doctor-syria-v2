from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from medical_records.models import Prescription
from medical_records.serializers import PrescriptionSerializer
from .models import Medicine, Inventory, Order, OrderItem, StockAlert, ExpiryAlert

User = get_user_model()


class MedicineSerializer(serializers.ModelSerializer):
    """
    مسلسل الأدوية
    """

    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicine
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    """
    مسلسل المخزون
    """

    medicine = MedicineSerializer(read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), write_only=True, source="medicine"
    )
    total_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Inventory
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """
    مسلسل عناصر الطلب
    """

    medicine = MedicineSerializer(read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), write_only=True, source="medicine"
    )

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    مسلسل الطلبات
    """

    patient = UserSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type="patient"),
        write_only=True,
        source="patient",
    )
    prescription = PrescriptionSerializer(read_only=True)
    prescription_id = serializers.PrimaryKeyRelatedField(
        queryset=Prescription.objects.all(),
        write_only=True,
        source="prescription",
        required=False,
        allow_null=True,
    )
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("final_amount",)

    def validate(self, data):
        """
        التحقق من صحة البيانات
        """
        if data.get("prescription") and not data["requires_prescription"]:
            raise serializers.ValidationError(
                _("لا يمكن إضافة وصفة طبية لطلب لا يتطلب وصفة")
            )
        return data


class StockAlertSerializer(serializers.ModelSerializer):
    """
    مسلسل تنبيهات المخزون
    """

    medicine = MedicineSerializer(read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), write_only=True, source="medicine"
    )

    class Meta:
        model = StockAlert
        fields = "__all__"
        read_only_fields = ("is_resolved", "resolved_at")


class ExpiryAlertSerializer(serializers.ModelSerializer):
    """
    مسلسل تنبيهات انتهاء الصلاحية
    """

    medicine = MedicineSerializer(read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), write_only=True, source="medicine"
    )

    class Meta:
        model = ExpiryAlert
        fields = "__all__"
        read_only_fields = ("is_resolved", "resolved_at")
