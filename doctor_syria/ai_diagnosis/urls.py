from django.urls import path

from . import views

app_name = "ai_diagnosis"

urlpatterns = [
    path("analyze/", views.AIAnalysisCreateView.as_view(), name="analyze"),
    path(
        "analyze/image/", views.ImageAnalysisCreateView.as_view(), name="analyze-image"
    ),
    path(
        "drug-interactions/",
        views.DrugInteractionCheckView.as_view(),
        name="drug-interactions",
    ),
    path(
        "results/<int:pk>/",
        views.AIAnalysisDetailView.as_view(),
        name="analysis-detail",
    ),
]
