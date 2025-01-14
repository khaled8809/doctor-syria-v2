from django.urls import path

from . import views

app_name = "decision_support"

urlpatterns = [
    path(
        "clinical-decisions/",
        views.ClinicalDecisionListView.as_view(),
        name="decision-list",
    ),
    path(
        "clinical-decisions/create/",
        views.ClinicalDecisionCreateView.as_view(),
        name="decision-create",
    ),
    path("protocols/", views.TreatmentProtocolListView.as_view(), name="protocol-list"),
    path(
        "lab-analysis/",
        views.LabResultAnalysisListView.as_view(),
        name="lab-analysis-list",
    ),
]
