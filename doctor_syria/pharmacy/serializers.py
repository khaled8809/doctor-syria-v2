from rest_framework import serializers
from .models import (Medicine, PharmacyInventory, MedicineOrder, OrderItem,
                    DeliveryAddress, MedicineCategory, MedicineCategoryRelation)
from accounts.serializers import PharmacySerializer, PharmaceuticalCompanySerializer

class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    manufacturer = PharmaceuticalCompanySerializer(read_only=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = '__all__'

    def get_categories(self, obj):
        category_relations = obj.categories.all()
        categories = [relation.category for relation in category_relations]
        return MedicineCategorySerializer(categories, many=True).data

class PharmacyInventorySerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    medicine = MedicineSerializer(read_only=True)

    class Meta:
        model = PharmacyInventory
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

class MedicineOrderSerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = MedicineOrder
        fields = '__all__'

class DeliveryAddressSerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)

    class Meta:
        model = DeliveryAddress
        fields = '__all__'

class MedicineCategoryRelationSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    category = MedicineCategorySerializer(read_only=True)

    class Meta:
        model = MedicineCategoryRelation
        fields = '__all__'
