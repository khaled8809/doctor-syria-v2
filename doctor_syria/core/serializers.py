"""
Core serializers for the project.
"""
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from pharmacy.models import Medicine, Prescription, PrescriptionItem

User = get_user_model()


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for all models.
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    updated_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        abstract = True
        fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]

    def get_field_names(self, declared_fields, info):
        """
        إضافة دعم لتحديد الحقول المطلوبة عبر معامل fields في URL
        مثال: ?fields=id,name,price
        """
        fields = self.context.get("request").query_params.get("fields")
        if fields:
            return fields.split(",")
        return super().get_field_names(declared_fields, info)

    def validate_empty_values(self, data):
        """
        التحقق من القيم الفارغة وتحويلها إلى None
        """
        for field in data:
            if data[field] == "":
                data[field] = None
        return super().validate_empty_values(data)

    def current_user(self):
        """
        الحصول على المستخدم الحالي من السياق
        """
        return self.context.get("request").user

    def create(self, validated_data):
        """
        إضافة المستخدم الحالي تلقائياً عند الإنشاء
        """
        validated_data["created_by"] = self.current_user()
        validated_data["updated_by"] = self.current_user()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        إضافة المستخدم الحالي تلقائياً عند التحديث
        """
        validated_data["updated_by"] = self.current_user()
        return super().update(instance, validated_data)


class MedicineListSerializer(serializers.ModelSerializer):
    """
    Serializer for medicine list.
    """
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'name_ar', 'price', 'quantity', 'is_active']


class PrescriptionSerializer(BaseModelSerializer):
    """
    Serializer for prescription.
    """
    class Meta:
        model = Prescription
        fields = BaseModelSerializer.Meta.fields + [
            'patient',
            'notes',
            'is_filled',
        ]


class PrescriptionItemSerializer(BaseModelSerializer):
    """
    Serializer for prescription item.
    """
    medicine_detail = MedicineListSerializer(source='medicine', read_only=True)

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
