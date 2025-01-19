"""
URLs configuration for the medical records application.

This module defines all URL patterns for the medical records app, including:
- Medical record management
- Patient history tracking
- Allergies and vaccinations
- Medical document management
"""
from django.urls import include, path

from core.api.routers import create_router
from . import views

app_name = "medical_records"

# Create router with app-specific settings
router = create_router(app_name)

# السجلات الطبية والتاريخ المرضي
router.register(
    r'records',
    views.MedicalRecordViewSet,
    basename='record'
)
router.register(
    r'history',
    views.PatientHistoryViewSet,
    basename='history'
)

# الحساسية والتطعيمات
router.register(
    r'allergies',
    views.AllergyViewSet,
    basename='allergy'
)
router.register(
    r'vaccinations',
    views.VaccinationViewSet,
    basename='vaccination'
)

# المستندات الطبية
router.register(
    r'documents',
    views.MedicalDocumentViewSet,
    basename='document'
)

# Define URL patterns
urlpatterns = [
    # API URLs - يشمل جميع نقاط النهاية للـ API
    path('api/v1/', include((router.urls, app_name), namespace='api')),
    
    # Web URLs - روابط واجهة المستخدم
    path('records/', include([
        path('', views.RecordListView.as_view(), name='record_list'),
        path('create/', views.RecordCreateView.as_view(), name='record_create'),
        path('<int:pk>/', include([
            path('', views.RecordDetailView.as_view(), name='record_detail'),
            path('update/', views.RecordUpdateView.as_view(), name='record_update'),
            path('delete/', views.RecordDeleteView.as_view(), name='record_delete'),
        ])),
    ])),
    
    # Print URLs - روابط الطباعة
    path('print/', include([
        path('record/<int:pk>/', views.PrintRecordView.as_view(), name='print_record'),
        path('history/<int:pk>/', views.PrintHistoryView.as_view(), name='print_history'),
    ])),
    
    # Export URLs - روابط التصدير
    path('export/', include([
        path('pdf/<int:pk>/', views.ExportPDFView.as_view(), name='export_pdf'),
        path('excel/<int:pk>/', views.ExportExcelView.as_view(), name='export_excel'),
    ])),
]
