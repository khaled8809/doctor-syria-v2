"""
URL configuration for pharmacy app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "pharmacy"

router = DefaultRouter()
router.register(r'medicines', views.MedicineViewSet)
router.register(r'prescriptions', views.PrescriptionViewSet)
router.register(r'prescription-items', views.PrescriptionItemViewSet)

# الأدوية والمخزون
router.register(
    r'inventory',
    views.InventoryViewSet,
    basename='inventory'
)
router.register(
    r'categories',
    views.MedicineCategoryViewSet,
    basename='category'
)

# الطلبات والمبيعات
router.register(
    r'orders',
    views.OrderViewSet,
    basename='order'
)
router.register(
    r'order-items',
    views.OrderItemViewSet,
    basename='order-item'
)

# التنبيهات والمراقبة
router.register(
    r'stock-alerts',
    views.StockAlertViewSet,
    basename='stock-alert'
)
router.register(
    r'expiry-alerts',
    views.ExpiryAlertViewSet,
    basename='expiry-alert'
)

# الموردين
router.register(
    r'suppliers',
    views.SupplierViewSet,
    basename='supplier'
)

# Define URL patterns
urlpatterns = [
    # API URLs - يشمل جميع نقاط النهاية للـ API
    path('api/v1/', include((router.urls, app_name), namespace='api')),
    
    # Web URLs - للواجهات التي تتطلب عرض صفحات
    path('inventory/', views.InventoryDashboardView.as_view(), name='inventory-dashboard'),
    path('orders/', views.OrderManagementView.as_view(), name='order-management'),
    path('reports/', views.PharmacyReportsView.as_view(), name='reports'),
    path('', include(router.urls)),
]
