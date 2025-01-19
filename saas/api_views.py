from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Invoice,
    Subscription,
    SubscriptionFeature,
    SubscriptionPlan,
    Tenant,
    TenantUser,
    Usage,
)
from .serializers import (
    InvoiceSerializer,
    SubscriptionFeatureSerializer,
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    TenantSerializer,
    TenantUserSerializer,
    UsageSerializer,
)


class BaseTenantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    def get_queryset(self):
        """
        تصفية النتائج حسب المستأجر الحالي
        """
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(tenant=self.request.tenant)


class TenantViewSet(BaseTenantViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["name", "subdomain"]
    ordering_fields = ["name", "created_at"]
    filterset_fields = ["is_active"]

    @swagger_auto_schema(
        operation_description="إحصائيات المستأجر",
        responses={200: openapi.Response("إحصائيات المستأجر")},
    )
    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        """
        إحصائيات استخدام المستأجر
        """
        tenant = self.get_object()
        stats = {
            "active_users": TenantUser.objects.filter(
                tenant=tenant, is_active=True
            ).count(),
            "total_usage": Usage.objects.filter(tenant=tenant).count(),
            "active_subscriptions": Subscription.objects.filter(
                tenant=tenant, status="active", end_date__gt=timezone.now()
            ).count(),
        }
        return Response(stats)


class TenantUserViewSet(BaseTenantViewSet):
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer
    search_fields = ["user__username", "user__email"]
    ordering_fields = ["user__date_joined"]
    filterset_fields = ["is_active", "role"]


class SubscriptionFeatureViewSet(BaseTenantViewSet):
    queryset = SubscriptionFeature.objects.all()
    serializer_class = SubscriptionFeatureSerializer
    search_fields = ["name", "code"]
    ordering_fields = ["name"]
    filterset_fields = ["is_active"]


class SubscriptionPlanViewSet(BaseTenantViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    filterset_fields = ["is_active", "billing_cycle"]


class SubscriptionViewSet(BaseTenantViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    search_fields = ["tenant__name"]
    ordering_fields = ["start_date", "end_date"]
    filterset_fields = ["status"]

    @swagger_auto_schema(
        operation_description="إلغاء الاشتراك",
        responses={200: openapi.Response("تم إلغاء الاشتراك بنجاح")},
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        إلغاء الاشتراك
        """
        subscription = self.get_object()
        subscription.status = "cancelled"
        subscription.save()
        return Response({"status": "تم إلغاء الاشتراك"})


class UsageViewSet(BaseTenantViewSet):
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer
    search_fields = ["feature__name"]
    ordering_fields = ["date", "count"]
    filterset_fields = ["feature"]


class InvoiceViewSet(BaseTenantViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    search_fields = ["tenant__name"]
    ordering_fields = ["due_date", "amount"]
    filterset_fields = ["status"]

    @swagger_auto_schema(
        operation_description="تحديث حالة الفاتورة إلى مدفوعة",
        responses={200: openapi.Response("تم تحديث حالة الفاتورة بنجاح")},
    )
    @action(detail=True, methods=["post"])
    def mark_as_paid(self, request, pk=None):
        """
        تحديث حالة الفاتورة إلى مدفوعة
        """
        invoice = self.get_object()
        invoice.status = "paid"
        invoice.paid_date = timezone.now()
        invoice.save()
        return Response({"status": "تم تحديث حالة الفاتورة إلى مدفوعة"})
