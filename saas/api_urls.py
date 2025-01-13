from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register(r"tenants", api_views.TenantViewSet)
router.register(r"tenant-users", api_views.TenantUserViewSet)
router.register(r"subscription-features", api_views.SubscriptionFeatureViewSet)
router.register(r"subscription-plans", api_views.SubscriptionPlanViewSet)
router.register(r"subscriptions", api_views.SubscriptionViewSet)
router.register(r"usage", api_views.UsageViewSet)
router.register(r"invoices", api_views.InvoiceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
