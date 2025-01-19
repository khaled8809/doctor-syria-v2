from django.urls import path
from rest_framework import routers

from . import views

app_name = "preventive_care"

# API Router
router = routers.DefaultRouter()
router.register(r'checkups', views.PreventiveCheckupViewSet)
router.register(r'vaccinations', views.VaccinationViewSet)
router.register(r'screenings', views.ScreeningViewSet)
router.register(r'health-tips', views.HealthTipViewSet)

urlpatterns = [
    # Home and Dashboard
    path("", views.PreventiveCareHomeView.as_view(), name="home"),
    path("dashboard/", views.PreventiveCareDashboardView.as_view(), name="dashboard"),
    
    # Checkups
    path("checkups/", views.PreventiveCheckupListView.as_view(), name="checkup_list"),
    path("checkups/create/", views.PreventiveCheckupCreateView.as_view(), name="checkup_create"),
    path("checkups/<int:pk>/", views.PreventiveCheckupDetailView.as_view(), name="checkup_detail"),
    path("checkups/schedule/", views.CheckupScheduleView.as_view(), name="checkup_schedule"),
    path("checkups/reminders/", views.CheckupReminderView.as_view(), name="checkup_reminders"),
    
    # Vaccinations
    path("vaccinations/", views.VaccinationListView.as_view(), name="vaccination_list"),
    path("vaccinations/create/", views.VaccinationCreateView.as_view(), name="vaccination_create"),
    path("vaccinations/<int:pk>/", views.VaccinationDetailView.as_view(), name="vaccination_detail"),
    path("vaccinations/schedule/", views.VaccinationScheduleView.as_view(), name="vaccination_schedule"),
    path("vaccinations/calendar/", views.VaccinationCalendarView.as_view(), name="vaccination_calendar"),
    
    # Health Screenings
    path("screenings/", views.HealthScreeningListView.as_view(), name="screening_list"),
    path("screenings/create/", views.HealthScreeningCreateView.as_view(), name="screening_create"),
    path("screenings/<int:pk>/", views.HealthScreeningDetailView.as_view(), name="screening_detail"),
    path("screenings/recommendations/", views.ScreeningRecommendationsView.as_view(), name="screening_recommendations"),
    
    # Health Education
    path("health-tips/", views.HealthTipListView.as_view(), name="health_tip_list"),
    path("health-tips/<int:pk>/", views.HealthTipDetailView.as_view(), name="health_tip_detail"),
    path("health-tips/categories/", views.HealthTipCategoryView.as_view(), name="health_tip_categories"),
    path("education/materials/", views.EducationalMaterialView.as_view(), name="educational_materials"),
    
    # Risk Assessment
    path("risk-assessment/", views.RiskAssessmentView.as_view(), name="risk_assessment"),
    path("risk-factors/", views.RiskFactorView.as_view(), name="risk_factors"),
    path("lifestyle/assessment/", views.LifestyleAssessmentView.as_view(), name="lifestyle_assessment"),
    
    # Reports and Analytics
    path("reports/", views.PreventiveCareReportView.as_view(), name="reports"),
    path("analytics/", views.PreventiveCareAnalyticsView.as_view(), name="analytics"),
    path("statistics/", views.PreventiveCareStatsView.as_view(), name="statistics"),
    
    # Notifications and Reminders
    path("notifications/", views.NotificationSettingsView.as_view(), name="notifications"),
    path("reminders/", views.ReminderSettingsView.as_view(), name="reminders"),
    path("alerts/", views.AlertSettingsView.as_view(), name="alerts"),
]

urlpatterns += router.urls
