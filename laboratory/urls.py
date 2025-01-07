from django.urls import path
from . import views

app_name = 'laboratory'

urlpatterns = [
    # إدارة التحاليل
    path('tests/', views.TestListView.as_view(), name='test-list'),
    path('tests/create/', views.TestCreateView.as_view(), name='test-create'),
    path('tests/<int:pk>/', views.TestDetailView.as_view(), name='test-detail'),
    path('tests/<int:pk>/update/', views.TestUpdateView.as_view(), name='test-update'),
    path('tests/<int:pk>/delete/', views.TestDeleteView.as_view(), name='test-delete'),
    
    # طلبات التحاليل
    path('requests/', views.TestRequestListView.as_view(), name='request-list'),
    path('requests/create/', views.TestRequestCreateView.as_view(), name='request-create'),
    path('requests/<int:pk>/', views.TestRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:pk>/update/', views.TestRequestUpdateView.as_view(), name='request-update'),
    path('requests/<int:pk>/delete/', views.TestRequestDeleteView.as_view(), name='request-delete'),
    path('requests/<int:pk>/process/', views.TestRequestProcessView.as_view(), name='request-process'),
    
    # النتائج
    path('results/', views.TestResultListView.as_view(), name='result-list'),
    path('results/<int:pk>/', views.TestResultDetailView.as_view(), name='result-detail'),
    path('results/<int:pk>/pdf/', views.TestResultPDFView.as_view(), name='result-pdf'),
    
    # التقارير والإحصائيات
    path('reports/', views.LaboratoryReportView.as_view(), name='reports'),
    path('reports/daily/', views.DailyReportView.as_view(), name='daily-report'),
    path('reports/monthly/', views.MonthlyReportView.as_view(), name='monthly-report'),
    
    # البحث
    path('search/', views.LaboratorySearchView.as_view(), name='search'),
]
