"""
URLs configuration for the laboratory application.

This module defines all URL patterns for the laboratory app, including:
- Lab test management
- Test requests and results
- Sample collection
- Laboratory management
"""
from django.urls import include, path

from core.api.routers import create_router
from . import views

app_name = "laboratory"

# Create router with app-specific settings
router = create_router(app_name)

# الفحوصات والفئات
router.register(
    r'tests',
    views.LabTestViewSet,
    basename='test'
)
router.register(
    r'categories',
    views.TestCategoryViewSet,
    basename='category'
)
router.register(
    r'reference-ranges',
    views.ReferenceRangeViewSet,
    basename='reference-range'
)

# طلبات الفحص والنتائج
router.register(
    r'test-requests',
    views.TestRequestViewSet,
    basename='test-request'
)
router.register(
    r'test-results',
    views.TestResultViewSet,
    basename='test-result'
)

# جمع العينات
router.register(
    r'sample-collections',
    views.SampleCollectionViewSet,
    basename='sample-collection'
)

# المختبرات
router.register(
    r'laboratories',
    views.LaboratoryViewSet,
    basename='laboratory'
)

# Define URL patterns
urlpatterns = [
    # API URLs - يشمل جميع نقاط النهاية للـ API
    path('api/v1/', include((router.urls, app_name), namespace='api')),
    
    # Web URLs - للواجهات التي تتطلب عرض صفحات
    path('dashboard/', views.LaboratoryDashboardView.as_view(), name='dashboard'),
    path('tests/', views.TestManagementView.as_view(), name='test-management'),
    path('samples/', views.SampleManagementView.as_view(), name='sample-management'),
    path('results/', views.ResultManagementView.as_view(), name='result-management'),
    path('reports/', views.LaboratoryReportsView.as_view(), name='reports'),
    
    # Print URLs - لطباعة النتائج والتقارير
    path('print/result/<int:pk>/', views.PrintTestResultView.as_view(), name='print-result'),
    path('print/report/<str:report_type>/', views.PrintReportView.as_view(), name='print-report'),
]
