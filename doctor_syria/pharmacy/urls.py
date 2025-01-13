from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ExpiryAlertViewSet,
    InventoryViewSet,
    MedicineViewSet,
    OrderItemViewSet,
    OrderViewSet,
    StockAlertViewSet,
)

router = DefaultRouter()
router.register("medicines", MedicineViewSet)
router.register("inventory", InventoryViewSet)
router.register("orders", OrderViewSet)
router.register("order-items", OrderItemViewSet)
router.register("stock-alerts", StockAlertViewSet)
router.register("expiry-alerts", ExpiryAlertViewSet)

app_name = "pharmacy"

urlpatterns = [
    path("api/", include(router.urls)),
]
