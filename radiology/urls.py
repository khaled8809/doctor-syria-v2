from django.urls import path
from . import views

app_name = 'radiology'

urlpatterns = [
    # إدارة الفحوصات الإشعاعية
    path('examinations/', views.ExaminationListView.as_view(), name='examination-list'),
    path('examinations/create/', views.ExaminationCreateView.as_view(), name='examination-create'),
    path('examinations/<int:pk>/', views.ExaminationDetailView.as_view(), name='examination-detail'),
    path('examinations/<int:pk>/update/', views.ExaminationUpdateView.as_view(), name='examination-update'),
    path('examinations/<int:pk>/delete/', views.ExaminationDeleteView.as_view(), name='examination-delete'),
    
    # طلبات الأشعة
    path('requests/', views.RadiologyRequestListView.as_view(), name='request-list'),
    path('requests/create/', views.RadiologyRequestCreateView.as_view(), name='request-create'),
    path('requests/<int:pk>/', views.RadiologyRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:pk>/update/', views.RadiologyRequestUpdateView.as_view(), name='request-update'),
    path('requests/<int:pk>/delete/', views.RadiologyRequestDeleteView.as_view(), name='request-delete'),
    path('requests/<int:pk>/process/', views.RadiologyRequestProcessView.as_view(), name='request-process'),
    
    # النتائج والتقارير
    path('results/', views.RadiologyResultListView.as_view(), name='result-list'),
    path('results/<int:pk>/', views.RadiologyResultDetailView.as_view(), name='result-detail'),
    path('results/<int:pk>/pdf/', views.RadiologyResultPDFView.as_view(), name='result-pdf'),
    path('results/<int:pk>/images/', views.RadiologyImagesView.as_view(), name='result-images'),
    
    # إدارة الأجهزة
    path('equipment/', views.RadiologyEquipmentListView.as_view(), name='equipment-list'),
    path('equipment/create/', views.RadiologyEquipmentCreateView.as_view(), name='equipment-create'),
    path('equipment/<int:pk>/', views.RadiologyEquipmentDetailView.as_view(), name='equipment-detail'),
    path('equipment/<int:pk>/update/', views.RadiologyEquipmentUpdateView.as_view(), name='equipment-update'),
    path('equipment/<int:pk>/delete/', views.RadiologyEquipmentDeleteView.as_view(), name='equipment-delete'),
    path('equipment/<int:pk>/maintenance/', views.EquipmentMaintenanceView.as_view(), name='equipment-maintenance'),
    
    # التقارير والإحصائيات
    path('reports/', views.RadiologyReportView.as_view(), name='reports'),
    path('reports/daily/', views.DailyReportView.as_view(), name='daily-report'),
    path('reports/monthly/', views.MonthlyReportView.as_view(), name='monthly-report'),
    path('reports/equipment/', views.EquipmentReportView.as_view(), name='equipment-report'),
    
    # البحث
    path('search/', views.RadiologySearchView.as_view(), name='search'),
    
    # الجدولة
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('schedule/<int:year>/<int:month>/<int:day>/', views.DayScheduleView.as_view(), name='day-schedule'),
]
