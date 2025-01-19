from django.urls import path
from rest_framework import routers

from . import views

app_name = "ai_diagnosis"

# API Router
router = routers.DefaultRouter()
router.register(r'analyses', views.AIAnalysisViewSet)
router.register(r'symptoms', views.SymptomViewSet)
router.register(r'conditions', views.MedicalConditionViewSet)
router.register(r'models', views.AIModelViewSet)

urlpatterns = [
    # General Analysis
    path("analyze/", views.AIAnalysisCreateView.as_view(), name="analyze"),
    path("analyze/symptoms/", views.SymptomAnalysisView.as_view(), name="analyze-symptoms"),
    path("analyze/history/", views.HistoryAnalysisView.as_view(), name="analyze-history"),
    path("results/<int:pk>/", views.AIAnalysisDetailView.as_view(), name="analysis-detail"),
    path("results/export/", views.AnalysisExportView.as_view(), name="analysis-export"),
    
    # Image Analysis
    path("analyze/image/", views.ImageAnalysisCreateView.as_view(), name="analyze-image"),
    path("analyze/xray/", views.XRayAnalysisView.as_view(), name="analyze-xray"),
    path("analyze/mri/", views.MRIAnalysisView.as_view(), name="analyze-mri"),
    path("analyze/ct/", views.CTScanAnalysisView.as_view(), name="analyze-ct"),
    
    # Drug Related
    path("drug-interactions/", views.DrugInteractionCheckView.as_view(), name="drug-interactions"),
    path("drug-recommendations/", views.DrugRecommendationView.as_view(), name="drug-recommendations"),
    path("dosage-optimization/", views.DosageOptimizationView.as_view(), name="dosage-optimization"),
    
    # Risk Assessment
    path("risk-assessment/", views.RiskAssessmentView.as_view(), name="risk-assessment"),
    path("risk-factors/", views.RiskFactorsView.as_view(), name="risk-factors"),
    path("prevention-recommendations/", views.PreventionRecommendationsView.as_view(), name="prevention-recommendations"),
    
    # AI Models
    path("models/", views.AIModelListView.as_view(), name="model-list"),
    path("models/<int:pk>/", views.AIModelDetailView.as_view(), name="model-detail"),
    path("models/train/", views.ModelTrainingView.as_view(), name="model-train"),
    path("models/evaluate/", views.ModelEvaluationView.as_view(), name="model-evaluate"),
    
    # Dashboard and Analytics
    path("dashboard/", views.AIDashboardView.as_view(), name="dashboard"),
    path("analytics/accuracy/", views.AccuracyAnalyticsView.as_view(), name="accuracy-analytics"),
    path("analytics/usage/", views.UsageAnalyticsView.as_view(), name="usage-analytics"),
    
    # Settings and Configuration
    path("settings/", views.AISettingsView.as_view(), name="settings"),
    path("settings/thresholds/", views.ThresholdSettingsView.as_view(), name="threshold-settings"),
    path("settings/notifications/", views.NotificationSettingsView.as_view(), name="notification-settings"),
]

urlpatterns += router.urls
