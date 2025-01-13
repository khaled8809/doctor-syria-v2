from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, Q
from .models import Medicine, Inventory, Order, OrderItem, StockAlert, ExpiryAlert
from .serializers import (
    MedicineSerializer,
    InventorySerializer,
    OrderSerializer,
    OrderItemSerializer,
    StockAlertSerializer,
    ExpiryAlertSerializer,
)
from .filters import (
    MedicineFilter,
    InventoryFilter,
    OrderFilter,
    OrderItemFilter,
    StockAlertFilter,
    ExpiryAlertFilter,
)


class MedicineViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر الأدوية
    """

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filterset_class = MedicineFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "scientific_name", "manufacturer"]
    ordering_fields = ["name", "price", "created_at"]

    @action(detail=False, methods=["get"])
    def expired(self, request):
        """
        الأدوية منتهية الصلاحية
        """
        queryset = self.get_queryset().filter(expiry_date__lte=timezone.now().date())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """
        الأدوية منخفضة المخزون
        """
        queryset = (
            self.get_queryset()
            .annotate(total_quantity=Sum("inventory_records__quantity"))
            .filter(
                Q(total_quantity__lte=F("min_quantity"))
                | Q(total_quantity__isnull=True)
            )
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InventoryViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر المخزون
    """

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filterset_class = InventoryFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["medicine__name", "batch_number", "supplier"]
    ordering_fields = ["expiry_date", "quantity", "created_at"]

    @action(detail=False, methods=["get"])
    def expiring_soon(self, request):
        """
        الأدوية التي ستنتهي صلاحيتها قريباً
        """
        threshold_date = timezone.now().date() + timezone.timedelta(days=90)
        queryset = self.get_queryset().filter(
            expiry_date__lte=threshold_date, expiry_date__gt=timezone.now().date()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر الطلبات
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["patient__name", "id"]
    ordering_fields = ["created_at", "total_amount"]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        إلغاء الطلب
        """
        order = self.get_object()
        if order.status not in ["pending", "confirmed"]:
            return Response(
                {"detail": _("لا يمكن إلغاء هذا الطلب في حالته الحالية")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = "cancelled"
        order.save()
        return Response({"detail": _("تم إلغاء الطلب بنجاح")})

    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        """
        معالجة الطلب
        """
        order = self.get_object()
        if order.status != "confirmed":
            return Response(
                {"detail": _("لا يمكن معالجة هذا الطلب في حالته الحالية")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = "processing"
        order.save()
        return Response({"detail": _("تم بدء معالجة الطلب بنجاح")})


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر عناصر الطلب
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_class = OrderItemFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["medicine__name", "order__id"]
    ordering_fields = ["quantity", "total_price"]


class StockAlertViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر تنبيهات المخزون
    """

    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer
    filterset_class = StockAlertFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["medicine__name"]
    ordering_fields = ["created_at", "current_quantity"]

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        """
        حل التنبيه
        """
        alert = self.get_object()
        alert.resolve()
        return Response({"detail": _("تم حل التنبيه بنجاح")})


class ExpiryAlertViewSet(viewsets.ModelViewSet):
    """
    وجهة نظر تنبيهات انتهاء الصلاحية
    """

    queryset = ExpiryAlert.objects.all()
    serializer_class = ExpiryAlertSerializer
    filterset_class = ExpiryAlertFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["medicine__name", "batch_number"]
    ordering_fields = ["expiry_date", "created_at"]

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        """
        حل التنبيه
        """
        alert = self.get_object()
        alert.resolve(request.data.get("notes", ""))
        return Response({"detail": _("تم حل التنبيه بنجاح")})
