from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicineViewSet,
    InventoryViewSet,
    OrderViewSet,
    OrderItemViewSet,
    StockAlertViewSet,
    ExpiryAlertViewSet,
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
