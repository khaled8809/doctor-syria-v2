"""
Serializers for the pharmacy application.
"""
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.serializers import UserSerializer, PatientSerializer
from medical_records.serializers import PrescriptionSerializer as MedicalPrescriptionSerializer
from core.serializers import BaseModelSerializer
from .models import ExpiryAlert, Inventory, Medicine, Order, OrderItem, StockAlert, Prescription, PrescriptionItem

User = get_user_model()


class MedicineSerializer(BaseModelSerializer):
    """
    مسلسل الأدوية
    """

    class Meta:
        model = Medicine
        fields = BaseModelSerializer.Meta.fields + [
            'name',
            'name_ar',
            'category',
            'form',
            'manufacturer',
            'description',
            'dosage',
            'storage_condition',
            'price',
            'requires_prescription',
            'is_active',
            'image',
            'barcode',
            'expiry_date',
            'side_effects',
            'contraindications',
            'interactions',
            'notes',
        ]


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
    prescription = MedicalPrescriptionSerializer(read_only=True)
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


class PrescriptionSerializer(BaseModelSerializer):
    """
    Serializer for Prescription model.
    """
    patient = PatientSerializer(read_only=True)
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = BaseModelSerializer.Meta.fields + [
            'patient',
            'notes',
            'is_filled',
        ]


class PrescriptionItemSerializer(BaseModelSerializer):
    """
    Serializer for PrescriptionItem model.
    """
    medicine_detail = MedicineSerializer(source='medicine', read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = BaseModelSerializer.Meta.fields + [
            'prescription',
            'medicine',
            'medicine_detail',
            'quantity',
            'dosage',
            'instructions',
        ]
