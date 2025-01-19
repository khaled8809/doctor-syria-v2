import django_filters
from django.utils.translation import gettext_lazy as _

from .models import ExpiryAlert, Inventory, Medicine, Order, OrderItem, StockAlert


class MedicineFilter(django_filters.FilterSet):
    """
    فلتر الأدوية
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    scientific_name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.ChoiceFilter()
    form = django_filters.ChoiceFilter()
    manufacturer = django_filters.CharFilter(lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    requires_prescription = django_filters.BooleanFilter()
    is_available = django_filters.BooleanFilter()
    is_expired = django_filters.BooleanFilter(method="filter_expired")

    class Meta:
        model = Medicine
        fields = [
            "name",
            "scientific_name",
            "category",
            "form",
            "manufacturer",
            "requires_prescription",
            "is_available",
        ]

    def filter_expired(self, queryset, name, value):
        """
        تصفية الأدوية منتهية الصلاحية
        """
        from django.utils import timezone

        if value:
            return queryset.filter(expiry_date__lte=timezone.now().date())
        return queryset.filter(expiry_date__gt=timezone.now().date())


class InventoryFilter(django_filters.FilterSet):
    """
    فلتر المخزون
    """

    medicine = django_filters.CharFilter(
        field_name="medicine__name", lookup_expr="icontains"
    )
    batch_number = django_filters.CharFilter(lookup_expr="icontains")
    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    expiry_date_min = django_filters.DateFilter(
        field_name="expiry_date", lookup_expr="gte"
    )
    expiry_date_max = django_filters.DateFilter(
        field_name="expiry_date", lookup_expr="lte"
    )
    supplier = django_filters.CharFilter(lookup_expr="icontains")
    purchase_date_min = django_filters.DateFilter(
        field_name="purchase_date", lookup_expr="gte"
    )
    purchase_date_max = django_filters.DateFilter(
        field_name="purchase_date", lookup_expr="lte"
    )

    class Meta:
        model = Inventory
        fields = [
            "medicine",
            "batch_number",
            "supplier",
            "expiry_date",
            "purchase_date",
        ]


class OrderFilter(django_filters.FilterSet):
    """
    فلتر الطلبات
    """

    patient = django_filters.CharFilter(
        field_name="patient__name", lookup_expr="icontains"
    )
    status = django_filters.ChoiceFilter()
    payment_method = django_filters.ChoiceFilter()
    payment_status = django_filters.ChoiceFilter()
    created_at_min = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_max = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    total_amount_min = django_filters.NumberFilter(
        field_name="total_amount", lookup_expr="gte"
    )
    total_amount_max = django_filters.NumberFilter(
        field_name="total_amount", lookup_expr="lte"
    )

    class Meta:
        model = Order
        fields = ["patient", "status", "payment_method", "payment_status", "created_at"]


class OrderItemFilter(django_filters.FilterSet):
    """
    فلتر عناصر الطلب
    """

    order = django_filters.NumberFilter()
    medicine = django_filters.CharFilter(
        field_name="medicine__name", lookup_expr="icontains"
    )
    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    total_price_min = django_filters.NumberFilter(
        field_name="total_price", lookup_expr="gte"
    )
    total_price_max = django_filters.NumberFilter(
        field_name="total_price", lookup_expr="lte"
    )

    class Meta:
        model = OrderItem
        fields = ["order", "medicine", "quantity", "total_price"]


class StockAlertFilter(django_filters.FilterSet):
    """
    فلتر تنبيهات المخزون
    """

    medicine = django_filters.CharFilter(
        field_name="medicine__name", lookup_expr="icontains"
    )
    is_resolved = django_filters.BooleanFilter()
    created_at_min = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_max = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = StockAlert
        fields = ["medicine", "is_resolved", "created_at"]


class ExpiryAlertFilter(django_filters.FilterSet):
    """
    فلتر تنبيهات انتهاء الصلاحية
    """

    medicine = django_filters.CharFilter(
        field_name="medicine__name", lookup_expr="icontains"
    )
    batch_number = django_filters.CharFilter(lookup_expr="icontains")
    expiry_date_min = django_filters.DateFilter(
        field_name="expiry_date", lookup_expr="gte"
    )
    expiry_date_max = django_filters.DateFilter(
        field_name="expiry_date", lookup_expr="lte"
    )
    is_resolved = django_filters.BooleanFilter()

    class Meta:
        model = ExpiryAlert
        fields = ["medicine", "batch_number", "expiry_date", "is_resolved"]
