from django.urls import path
from rest_framework import routers

from . import views

app_name = "decision_support"

# API Router
router = routers.DefaultRouter()
router.register(r'decisions', views.ClinicalDecisionViewSet)
router.register(r'protocols', views.TreatmentProtocolViewSet)
router.register(r'guidelines', views.ClinicalGuidelineViewSet)
router.register(r'alerts', views.ClinicalAlertViewSet)

urlpatterns = [
    # Clinical Decisions
    path("clinical-decisions/", views.ClinicalDecisionListView.as_view(), name="decision-list"),
    path("clinical-decisions/create/", views.ClinicalDecisionCreateView.as_view(), name="decision-create"),
    path("clinical-decisions/<int:pk>/", views.ClinicalDecisionDetailView.as_view(), name="decision-detail"),
    path("clinical-decisions/history/", views.DecisionHistoryView.as_view(), name="decision-history"),
    path("clinical-decisions/analyze/", views.DecisionAnalysisView.as_view(), name="decision-analyze"),
    
    # Treatment Protocols
    path("protocols/", views.TreatmentProtocolListView.as_view(), name="protocol-list"),
    path("protocols/<int:pk>/", views.TreatmentProtocolDetailView.as_view(), name="protocol-detail"),
    path("protocols/create/", views.TreatmentProtocolCreateView.as_view(), name="protocol-create"),
    path("protocols/search/", views.ProtocolSearchView.as_view(), name="protocol-search"),
    path("protocols/categories/", views.ProtocolCategoryView.as_view(), name="protocol-categories"),
    
    # Clinical Guidelines
    path("guidelines/", views.ClinicalGuidelineListView.as_view(), name="guideline-list"),
    path("guidelines/<int:pk>/", views.ClinicalGuidelineDetailView.as_view(), name="guideline-detail"),
    path("guidelines/create/", views.ClinicalGuidelineCreateView.as_view(), name="guideline-create"),
    path("guidelines/search/", views.GuidelineSearchView.as_view(), name="guideline-search"),
    
    # Lab Analysis
    path("lab-analysis/", views.LabResultAnalysisListView.as_view(), name="lab-analysis-list"),
    path("lab-analysis/<int:pk>/", views.LabResultAnalysisDetailView.as_view(), name="lab-analysis-detail"),
    path("lab-analysis/interpret/", views.LabResultInterpretationView.as_view(), name="lab-interpretation"),
    path("lab-analysis/trends/", views.LabResultTrendsView.as_view(), name="lab-trends"),
    
    # Risk Assessment
    path("risk-assessment/", views.RiskAssessmentView.as_view(), name="risk-assessment"),
    path("risk-assessment/factors/", views.RiskFactorsView.as_view(), name="risk-factors"),
    path("risk-assessment/scores/", views.RiskScoresView.as_view(), name="risk-scores"),
    
    # Clinical Alerts
    path("alerts/", views.ClinicalAlertListView.as_view(), name="alert-list"),
    path("alerts/settings/", views.AlertSettingsView.as_view(), name="alert-settings"),
    path("alerts/rules/", views.AlertRulesView.as_view(), name="alert-rules"),
    
    # Evidence-Based Medicine
    path("evidence/", views.EvidenceBaseView.as_view(), name="evidence-base"),
    path("evidence/search/", views.EvidenceSearchView.as_view(), name="evidence-search"),
    path("evidence/recommendations/", views.EvidenceRecommendationsView.as_view(), name="evidence-recommendations"),
    
    # Analytics and Reports
    path("analytics/", views.DecisionAnalyticsView.as_view(), name="decision-analytics"),
    path("analytics/outcomes/", views.OutcomeAnalyticsView.as_view(), name="outcome-analytics"),
    path("reports/", views.DecisionReportsView.as_view(), name="decision-reports"),
    
    # Settings
    path("settings/", views.DecisionSupportSettingsView.as_view(), name="settings"),
    path("settings/preferences/", views.UserPreferencesView.as_view(), name="preferences"),
    path("settings/integrations/", views.SystemIntegrationsView.as_view(), name="integrations"),
]

urlpatterns += router.urls
