from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "analytics"

# API Router
router = routers.DefaultRouter()
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')
router.register(r'appointments', views.AppointmentAnalyticsViewSet, basename='appointment-analytics')
router.register(r'laboratory', views.LabAnalyticsViewSet, basename='lab-analytics')
router.register(r'medicines', views.MedicineAnalyticsViewSet, basename='medicine-analytics')
router.register(r'revenue', views.RevenueAnalyticsViewSet, basename='revenue-analytics')
router.register(r'users', views.UserAnalyticsViewSet, basename='user-analytics')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Export Endpoints
    path('export/csv/', views.CSVExportView.as_view(), name='csv-export'),
    path('export/excel/', views.ExcelExportView.as_view(), name='excel-export'),
    path('export/pdf/', views.PDFExportView.as_view(), name='pdf-export'),
]
